import math

import torch
from neural_commons.cf_nn import LRStrategy
from neural_commons.cf_nn.lrs import SlideLRS

_slide_factor = 10.0


class CrossEntropyLossLRS(LRStrategy):
    def __init__(self, min_loss: float = 0):
        super().__init__()
        self.slide_lrs = SlideLRS(min_loss=min_loss)

    def requires_second_derivative(self) -> bool:
        return False

    def get_residual(self, is_final: bool, output: torch.Tensor, loss: torch.Tensor, grad1: torch.Tensor,
                     final_output_size: int):
        output_size = math.prod(output.shape[1:])
        if is_final:
            lr = 1.0 * output_size
        else:
            factor_min = 1.0
            factor_max = 10.0
            partial_os = output_size / 2
            max_w = partial_os / (partial_os + final_output_size)
            factor = factor_min * (1 - max_w) + factor_max * max_w
            lr = factor * final_output_size
        return -lr * grad1

