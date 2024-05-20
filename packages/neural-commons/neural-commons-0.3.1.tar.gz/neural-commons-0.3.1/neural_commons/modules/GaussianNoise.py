import torch
from torch import nn


class GaussianNoise(nn.Module):
    def __init__(self, std: float = 0.01):
        super().__init__()
        self.std = std

    def forward(self, x: torch.Tensor):
        if self.training:
            return x + torch.randn_like(x) * self.std
        return x
