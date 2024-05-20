import logging
import torch
from neural_commons.cf_nn import LRStrategy
from neural_commons.helpers.torch_helper import view_dims, dims_from, num_dims

_logger = logging.getLogger("neural-commons")


class SlideLRS(LRStrategy):
    def __init__(self, min_loss: float, deficit_factor: float = 1.0):
        super().__init__()
        if deficit_factor <= 0 or deficit_factor > 1:
            raise ValueError("final_factor must be in ]0, 1].")
        self.deficit_factor = deficit_factor
        self.min_loss = min_loss
        self.warned_low_loss = False

    def requires_second_derivative(self) -> bool:
        return False

    def get_residual(self, is_final: bool, output: torch.Tensor, loss: torch.Tensor, grad1: torch.Tensor,
                     final_output_size: int, eps=1e-30):
        # loss shape: (batch_size)
        deficit = loss - self.min_loss
        if torch.any(deficit < 0).item():
            deficit = torch.clamp(deficit, min=0)
            if not self.warned_low_loss:
                _logger.warning(f"SlideLRS: Loss contains a value less than min_loss ({self.min_loss}).")
                self.warned_low_loss = True
        deficit *= self.deficit_factor
        denominator = torch.clamp(torch.sum(grad1.pow(2), dim=dims_from(grad1)), min=eps)
        lr = deficit / denominator
        # lr shape: (batch_size)
        return -view_dims(lr, num_dims(grad1)) * grad1
