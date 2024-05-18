from torch.nn import Module
import numpy as np
import torch
from typing import Callable, Iterable
from collections import OrderedDict
from copy import deepcopy
import sys
sys.path.append(".")
sys.path.append("..")

from ..data import FastDataLoader  # NOQA
from ..client import Client  # NOQA
from ..utils import OptimizerConfigurator, clear_cache  # NOQA
from ..utils.model import STATE_DICT_KEYS_TO_IGNORE, safe_load_state_dict  # NOQA
from ..server import Server  # NOQA
from ..comm import Message  # NOQA
from . import CentralizedFL  # NOQA


def get_all_params_of(model, copy=True) -> torch.Tensor:
    result = None
    for param in model.parameters():
        if result is None:
            result = param.clone().detach().reshape(-1) if copy else param.reshape(-1)
        else:
            result = torch.cat((result, param.clone().detach().reshape(-1)),
                               0) if copy else torch.cat((result, param.reshape(-1)), 0)
    return result


def load_all_params(device, model, params):
    dict_param = deepcopy(dict(model.named_parameters()))
    idx = 0
    for name, param in model.named_parameters():
        weights = param.data
        length = len(weights.reshape(-1))
        dict_param[name].data.copy_(
            params[idx:idx+length].clone().detach().reshape(weights.shape).to(device))
        idx += length

    model.load_state_dict(dict_param)


class FedDynClient(Client):

    def __init__(self,
                 index: int,
                 train_set: FastDataLoader,
                 test_set: FastDataLoader,
                 optimizer_cfg: OptimizerConfigurator,
                 loss_fn: Callable,
                 local_epochs: int,
                 alpha: float):
        super().__init__(index, train_set, test_set, optimizer_cfg, loss_fn, local_epochs)

        self.hyper_params.update(alpha=alpha)
        self.weight = None
        self.weight_decay = self.optimizer_cfg.optimizer_cfg[
            "weight_decay"] if "weight_decay" in self.optimizer_cfg.optimizer_cfg else 0
        self.prev_grads = None

    def receive_model(self) -> None:
        model, cld_mdl = self.channel.receive(self, self.server, msg_type="model").payload
        if self.model is None:
            self.model = model
            self.prev_grads = torch.zeros_like(get_all_params_of(self.model))
        else:
            safe_load_state_dict(self.model, cld_mdl.state_dict())

    def _receive_weights(self) -> None:
        self.weight = self.channel.receive(self, self.server, msg_type="weight").payload

    def _send_weight(self) -> None:
        self.channel.send(Message(self.train_set.tensors[0].shape[0], "weight", self), self.server)

    def fit(self, override_local_epochs: int = 0):
        epochs = override_local_epochs if override_local_epochs else self.hyper_params.local_epochs
        self.receive_model()
        self.model.train()
        self.model.to(self.device)

        alpha_coef_adpt = self.hyper_params.alpha / self.weight
        server_params = get_all_params_of(self.model)

        for params in self.model.parameters():
            params.requires_grad = True

        if not self.optimizer:
            w_dec = alpha_coef_adpt + self.weight_decay
            self.optimizer, self.scheduler = self.optimizer_cfg(self.model,
                                                                # this override the weight_decay
                                                                # in the optimizer_cfg
                                                                weight_decay=w_dec)
        for _ in range(epochs):
            loss = None
            for _, (X, y) in enumerate(self.train_set):
                X, y = X.to(self.device), y.to(self.device)
                self.optimizer.zero_grad()
                y_hat = self.model(X)
                loss = self.hyper_params.loss_fn(y_hat, y)

                # Dynamic regularization
                curr_params = get_all_params_of(self.model, False)
                # penalty = -torch.sum(curr_params * self.prev_grads)
                # penalty += 0.5 * alpha_coef_adpt * torch.sum((curr_params - server_params) ** 2)
                penalty = alpha_coef_adpt * \
                    torch.sum(curr_params * (-server_params + self.prev_grads))
                loss = loss + penalty

                loss.backward()
                torch.nn.utils.clip_grad_norm_(parameters=self.model.parameters(), max_norm=10)
                self.optimizer.step()

            self.scheduler.step()

        # update the previous gradients
        curr_params = get_all_params_of(self.model)
        self.prev_grads += alpha_coef_adpt * (server_params - curr_params)

        self.model.to("cpu")
        clear_cache()
        self.send_model()


class FedDynServer(Server):
    def __init__(self,
                 model: Module,
                 test_data: FastDataLoader,
                 clients: Iterable[Client],
                 eval_every: int = 1,
                 weighted: bool = True,
                 alpha: float = 0.01):
        super().__init__(model, test_data, clients, eval_every, weighted)
        self.alpha = alpha
        self.cld_mdl = deepcopy(self.model)

    def broadcast_model(self, eligible: Iterable[Client]) -> None:
        self.channel.broadcast(Message((self.model, self.cld_mdl), "model", self), eligible)

    def fit(self, n_rounds: int = 10, eligible_perc: float = 0.1) -> None:

        # Weight computation
        for client in self.clients:
            client._send_weight()

        weights = np.array([self.channel.receive(
            self, client, msg_type="weight").payload for client in self.clients])
        weights = weights / np.sum(weights) * self.n_clients

        for i, client in enumerate(self.clients):
            self.channel.send(Message(weights[i], "weight", self), client)

        for client in self.clients:
            client._receive_weights()

        return super().fit(n_rounds, eligible_perc)

    @torch.no_grad()
    def aggregate(self, eligible: Iterable[Client]) -> None:
        avg_model_sd = OrderedDict()
        clients_sd = self.get_client_models(eligible, state_dict=False)
        weights = self._get_client_weights(eligible)

        for key in self.model.state_dict().keys():
            if key.endswith(STATE_DICT_KEYS_TO_IGNORE):
                avg_model_sd[key] = self.model.state_dict()[key].clone()
                continue
            for i, client_sd in enumerate(clients_sd):
                client_sd = client_sd.state_dict()
                if key not in avg_model_sd:
                    avg_model_sd[key] = weights[i] * client_sd[key]
                else:
                    avg_model_sd[key] += weights[i] * client_sd[key]

        avg_grad = None
        grad_count = 0
        for cl in self.clients:
            if cl.prev_grads is not None:
                grad_count += 1
                if avg_grad is None:
                    avg_grad = cl.prev_grads.clone().detach()
                else:
                    avg_grad += cl.prev_grads.clone().detach()

        if grad_count > 0:
            avg_grad /= grad_count

        self.model.load_state_dict(avg_model_sd)
        load_all_params(self.device, self.cld_mdl, get_all_params_of(self.model) + avg_grad)


class FedDyn(CentralizedFL):

    def get_client_class(self) -> Client:
        return FedDynClient

    def get_server_class(self) -> Server:
        return FedDynServer
