from typing import Union

import torch
from torch import nn


class Plus(nn.Module):
    def __init__(self, offset: Union[torch.Tensor, float]):
        super().__init__()
        self.offset = offset

    def forward(self, x: torch.Tensor):
        return x + self.offset
