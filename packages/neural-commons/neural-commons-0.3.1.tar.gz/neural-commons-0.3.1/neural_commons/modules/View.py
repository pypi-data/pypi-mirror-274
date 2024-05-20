import torch
from torch import nn


class View(nn.Module):
    def __init__(self, *dims: int):
        super().__init__()
        self.dims = dims

    def forward(self, x: torch.Tensor):
        return x.view(self.dims)
