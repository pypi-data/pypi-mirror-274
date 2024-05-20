import logging
import math
import torch
from torch import autograd
from neural_commons.cf_nn import LRStrategy

_logger = logging.getLogger("neural-commons")
_max_base_factor = 1.5
_min_base_factor = 0.5
_sd_mean_ts = 0.01


class AdaptiveLRS(LRStrategy):
    def __init__(self, min_loss: float = 0, deficit_factor: float = 1.0):
        super().__init__()
        self.min_loss = min_loss
        self.deficit_factor = deficit_factor
        self.warned_low_loss = False

    def requires_second_derivative(self) -> bool:
        return True

    def get_residual(self, is_final: bool, output: torch.Tensor, loss: torch.Tensor, grad1: torch.Tensor,
                     final_output_size: int) -> torch.Tensor:
        grad2 = autograd.grad(grad1.sum(), output)[0]
        if self.is_zero(grad2) or not self.is_flat(grad2):
            return self.get_slide_residual(loss, grad1)
        else:
            return self.get_newton_method_residual(grad1, grad2)

    def get_slide_residual(self, loss: torch.Tensor, grad1: torch.Tensor, eps=1e-15):
        deficit = loss.item() - self.min_loss
        if deficit < 0:
            deficit = 0
            if not self.warned_low_loss:
                _logger.warning(f"SlideLRS: Loss ({loss.item()}) is less than min_loss ({self.min_loss}).")
                self.warned_low_loss = True
        deficit *= self.deficit_factor
        denominator = torch.clamp(torch.sum(grad1.pow(2)), min=eps)
        lr = (deficit / denominator).item()
        return -lr * grad1

    @staticmethod
    def get_newton_method_residual(grad1: torch.Tensor,
                                   grad2: torch.Tensor):
        return -grad1 / grad2

    @staticmethod
    def is_zero(tensor: torch.Tensor) -> bool:
        return torch.all(torch.abs(tensor) <= 1e-20).item()

    @staticmethod
    def is_flat(tensor: torch.Tensor) -> bool:
        if torch.numel(tensor) < 3 or torch.any(tensor <= 0).item():
            return False
        t_mean = torch.mean(tensor).item()
        t_std = torch.std(tensor).item()
        return t_std / t_mean <= _sd_mean_ts

    @staticmethod
    def get_base_lr(is_final: bool, output: torch.Tensor,
                    final_output_size: int):
        batch_size = output.size(0)
        output_size = math.prod(output.shape[1:])
        fos = output_size if is_final else final_output_size
        base_result = 0.5 * batch_size * fos
        if is_final:
            lr = base_result
        else:
            factor_min = 1.0
            factor_max = 12.0
            partial_os = output_size / 2
            max_w = partial_os / (partial_os + final_output_size)
            factor = factor_min * (1 - max_w) + factor_max * max_w
            lr = factor * base_result
        return lr
