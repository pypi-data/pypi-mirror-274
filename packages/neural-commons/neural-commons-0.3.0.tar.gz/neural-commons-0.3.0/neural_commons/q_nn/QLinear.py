import math
import torch
import torch.nn.functional as F
from torch import nn

from neural_commons.q_nn import ParamModule

_sqrt_2 = math.sqrt(2)


class QLinear(nn.Module):
    __constants__ = ["in_features", "out_features"]

    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        scale = math.sqrt(in_features)
        if bias:
            scale *= _sqrt_2
        weight = torch.randn((out_features, in_features)) / scale
        bias_param = torch.randn((out_features,)) / _sqrt_2 if bias else None
        p_tensors = [weight]
        if bias_param is not None:
            p_tensors.append(bias_param)
        self.p_module = ParamModule(*p_tensors)
        self.bias = bias
        self.in_features = in_features
        self.out_features = out_features

    def forward(self, x: torch.Tensor):
        if self.bias:
            w, b = self.p_module()
        else:
            w = self.p_module()[0]
            b = None
        return F.linear(x, w, b)

    def extra_repr(self) -> str:
        return f'in_features={self.in_features}, out_features={self.out_features}, bias={self.bias}'
