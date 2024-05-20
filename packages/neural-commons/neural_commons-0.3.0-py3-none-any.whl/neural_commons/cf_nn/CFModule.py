import torch
from abc import abstractmethod
from torch import nn


class CFModule(nn.Module):
    def __init__(self, initial_lr_factor: float = 0.5, max_lr_factor: float = 1.0, alpha: float = 0.5, norm_output: bool = True):
        super().__init__()
        self.max_lr_factor = max_lr_factor
        self.norm_output = norm_output
        self.lr_factor_ma = initial_lr_factor
        self.alpha = alpha

    def update_lr_factor(self, new_lr_factor: float):
        new_lr_factor_ma = new_lr_factor * self.alpha + self.lr_factor_ma * (1 - self.alpha)
        self.lr_factor_ma = min(self.max_lr_factor, new_lr_factor_ma)

    @abstractmethod
    def cf_learn(self, inputs: tuple[torch.Tensor, ...], output: torch.Tensor, residual: torch.Tensor, **kwargs):
        """
        Applies a (closed-form) learning algorithm that changes the parameters of the module instance.
        Args:
            inputs: The inputs provided to the module.
            output: The original output of the module.
            residual: The residuals that should be added to the original output to obtain the desired output.
            **kwargs: Custom parameters of the learning algorithm.
        """
        pass
