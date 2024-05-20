import math
from typing import Iterable, Protocol, Union, Optional
import torch
from torch import autograd, nn

from neural_commons.cf_nn import CFModule
from neural_commons.helpers.torch_helper import concatenate_tensors, rms


class _TLossFn1(Protocol):
    def __call__(self) -> torch.Tensor:
        ...


class _TLossFn2(Protocol):
    def __call__(self, **kwargs) -> torch.Tensor:
        ...


_TLossFn = Union[_TLossFn1, _TLossFn2]


class InvalidCFStateException(BaseException):
    def __init__(self, msg: str):
        super().__init__(msg)


class CFOptimizer:
    def __init__(self, cf_modules: Iterable[CFModule], stochastic_selection: bool = False):
        self.cf_modules = list(cf_modules)
        if len(self.cf_modules) == 0:
            raise ValueError("Empty collection of ParamModules provided.")
        self.selected_index = -1
        self.selected_module: Optional[CFModule] = None
        self.stochastic_selection = stochastic_selection
        self.data_queue: list[tuple[tuple[torch.Tensor, ...], torch.Tensor, torch.Tensor]] = list()
        self._select_next()

    def _full_loss(self, base_loss: torch.Tensor, output: torch.Tensor, std_lambda: float):
        if not self.selected_module.norm_output:
            return base_loss
        extra_loss = (torch.std(output) - 1.0).pow(2) * std_lambda
        return base_loss + extra_loss

    def _grad_pass(self, fwd_fn: _TLossFn, std_lambda: float,
                   **kwargs) -> tuple[torch.Tensor, list[tuple[tuple[torch.Tensor, ...], torch.Tensor, torch.Tensor]]]:
        # Returns list of (input, output, grad)
        inout_list = list()

        def _hook(m: nn.Module, _inputs: tuple[torch.Tensor, ...], _output: torch.Tensor):
            new_output = _output.requires_grad_()
            _in_tuple = tuple(t.detach() for t in _inputs)
            inout_list.append((_in_tuple, new_output,))
            return new_output

        sm = self.selected_module
        h = sm.register_forward_hook(_hook)
        try:
            loss = fwd_fn(**kwargs)
        finally:
            h.remove()

        result = list()
        for inputs, output in inout_list:
            full_loss = self._full_loss(loss, output, std_lambda)
            grad1 = autograd.grad(full_loss, output)[0]
            result.append((inputs, output.detach(), grad1.detach()))
        return loss, result,

    def _lr_loss_grad(self, fwd_fn: _TLossFn, gradients: list[torch.Tensor],
                      lr: float, std_lambda: float, **kwargs) -> tuple[float, float]:
        # Returns loss and LR gradient
        gradient_count = len(gradients)
        lr_t_list = list()

        def _hook(m: nn.Module, _inputs: tuple[torch.Tensor, ...], _output: torch.Tensor):
            index = len(lr_t_list)
            if index >= gradient_count:
                raise InvalidCFStateException("List of gradients obtained in prior forward "
                                              "pass is shorter than the number of module "
                                              "visits in current pass.")
            lr_t = torch.tensor(lr, dtype=torch.float, device=_output.device).requires_grad_()
            new_output = _output - lr_t * gradients[index]
            lr_t_list.append((new_output, lr_t,))
            return new_output

        h = self.selected_module.register_forward_hook(_hook)
        try:
            loss = fwd_fn(**kwargs)
        finally:
            h.remove()

        lr_count = len(lr_t_list)
        if lr_count != gradient_count:
            raise InvalidCFStateException("The number of module visits in current forward pass "
                                          "does not match those of prior pass.")
        sum_grad = 0
        full_loss_sum = 0
        for output, lr_tensor in lr_t_list:
            full_loss = self._full_loss(loss, output, std_lambda)
            grad1 = autograd.grad(full_loss, lr_tensor)[0]
            sum_grad += grad1.item()
            full_loss_sum += full_loss.item()
        return full_loss_sum / lr_count, sum_grad / lr_count,

    def _simple_loss(self, fwd_fn: _TLossFn, gradients: list[torch.Tensor],
                     lr: float, std_lambda: float, **kwargs) -> float:
        gradient_count = len(gradients)
        out_list = list()

        def _hook(m: nn.Module, _inputs: tuple[torch.Tensor, ...], _output: torch.Tensor):
            index = len(out_list)
            if index >= gradient_count:
                raise InvalidCFStateException("List of gradients obtained in prior forward "
                                              "pass is shorter than the number of module "
                                              "visits in current pass.")
            new_output = _output - lr * gradients[index]
            out_list.append(new_output)
            return new_output

        with torch.no_grad():
            h = self.selected_module.register_forward_hook(_hook)
            try:
                loss = fwd_fn(**kwargs)
            finally:
                h.remove()
            num_outputs = len(out_list)
            if num_outputs != gradient_count:
                raise InvalidCFStateException("The number of module visits in current forward pass "
                                              "does not match those of prior pass.")
            full_loss_sum = 0
            for output in out_list:
                full_loss = self._full_loss(loss, output, std_lambda)
                full_loss_sum += full_loss.item()
            return full_loss_sum / num_outputs

    @staticmethod
    def _optimal_lr(lr1: float, lr2: float, lr_loss1: float, lr_loss2: float,
                    lr_grad1: float, lr_grad2: float, lr_expansion=2.0,
                    grad_reduction_threshold=0.03) -> tuple[float, Optional[float]]:
        if math.isinf(lr_grad2) or math.isnan(lr_grad2):
            return lr1, 1.0 / lr_expansion,
        elif math.copysign(1, lr_grad1) != math.copysign(1, lr_grad2):
            # Secant root-finding method
            return (lr1 * lr_grad2 - lr2 * lr_grad1) / (lr_grad2 - lr_grad1), None,
        elif lr_loss2 == lr_loss1:
            return lr1, 1.0,
        elif lr_loss2 < lr_loss1:
            if abs(lr_grad2) < abs(lr_grad1) * grad_reduction_threshold:
                return lr2, 1.0,
            else:
                return lr2, lr_expansion,
        else:
            return lr1, 1.0 / lr_expansion,

    def _update_sm_lr(self, lr: float, prior_approx_lr: float, approx_lr_expansion: float,
                      out_size: int):
        if approx_lr_expansion is not None:
            new_approx_lr = prior_approx_lr * approx_lr_expansion
        else:
            new_approx_lr = lr
        self.selected_module.update_lr_factor(new_approx_lr / out_size)

    def _select_next(self):
        cf_modules = self.cf_modules
        num_modules = len(cf_modules)
        if self.stochastic_selection:
            m_lr = [m.lr_factor_ma for m in cf_modules]
            m_lr = torch.tensor(m_lr, dtype=torch.float)
            m_weight = torch.ones_like(m_lr)
            self.selected_index = torch.multinomial(m_weight, 1).item()
        else:
            self.selected_index = (self.selected_index + 1) % num_modules
        self.selected_module = cf_modules[self.selected_index]

    def enqueue_data(self, fwd_fn: _TLossFn, std_lambda: float = 0.0001,
                     lr_expansion=2.0, **kwargs) -> float:
        loss, pass_info = self._grad_pass(fwd_fn, std_lambda, **kwargs)
        loss = loss.item()
        gradients = [g for _, _, g in pass_info]
        outputs = [out for _, out, _ in pass_info]
        if len(outputs) == 0:
            raise InvalidCFStateException("CFModule instances not visited in forward pass.")
        sm = self.selected_module
        out_size = torch.numel(outputs[0])
        approx_lr = sm.lr_factor_ma * out_size
        lr1 = 0
        lr2 = approx_lr * 2.0
        lr_loss1, lr_grad1 = self._lr_loss_grad(fwd_fn, gradients, lr1, std_lambda, **kwargs)
        lr_loss2, lr_grad2 = self._lr_loss_grad(fwd_fn, gradients, lr2, std_lambda, **kwargs)
        opt_lr, approx_lr_expansion = self._optimal_lr(lr1, lr2, lr_loss1, lr_loss2, lr_grad1, lr_grad2)
        if approx_lr_expansion is None:
            opt_loss = self._simple_loss(fwd_fn, gradients, opt_lr, std_lambda, **kwargs)
            if opt_loss > lr_loss1:
                # Failed to decrease loss. Reduce approx LR.
                opt_lr = lr1
                approx_lr_expansion = 1.0 / lr_expansion
        self._update_sm_lr(opt_lr, approx_lr, approx_lr_expansion, out_size)
        if opt_lr != 0:
            for inputs, output, gradient in pass_info:
                residual = (-gradient * opt_lr).detach()
                self.data_queue.append((inputs, output, residual,))
        return loss

    @property
    def queued_batch_size(self) -> int:
        return sum(output.size(0) for _, output, _ in self.data_queue)

    def _step(self, update_rate: float, max_residual_rel_rms: float, **kwargs):
        if len(self.data_queue) == 0:
            raise InvalidCFStateException("No data has been queued. Call enqueue_data() before calling step().")
        inputs_list = [i for i, _, _ in self.data_queue]
        output_list = [out for _, out, _ in self.data_queue]
        residual_list = [res for _, _, res in self.data_queue]
        self.data_queue = list()
        with torch.no_grad():
            inputs = concatenate_tensors(inputs_list, dim=0)
            del inputs_list
            output = torch.cat(output_list, dim=0)
            del output_list
            residual = torch.cat(residual_list, dim=0)
            del residual_list
            residual *= update_rate
            max_res_rms = rms(output) * max_residual_rel_rms
            res_rms = rms(residual)
            if res_rms > max_res_rms:
                residual *= max_res_rms / res_rms
            self.selected_module.cf_learn(inputs, output, residual, **kwargs)

    def step(self, update_rate: float = 1.0, max_residual_rel_rms = 1.0, **kwargs):
        if update_rate <= 0 or update_rate > 1.0:
            raise ValueError("update_rate expected to be in ]0, 1].")
        try:
            self._step(update_rate, max_residual_rel_rms, **kwargs)
        finally:
            self.data_queue = list()
            self._select_next()
