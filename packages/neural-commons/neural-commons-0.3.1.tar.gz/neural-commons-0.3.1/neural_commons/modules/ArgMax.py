from typing import Union

import torch
from torch import nn


class ArgMax(nn.Module):
    def __init__(self, dim: Union[int, None] = -1):
        super().__init__()
        self.dim = dim

    def forward(self, x: torch.Tensor):
        return torch.argmax(x, dim=self.dim)
