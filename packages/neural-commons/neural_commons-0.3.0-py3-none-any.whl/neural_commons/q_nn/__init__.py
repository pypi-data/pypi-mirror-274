import torch
from typing import Iterable
from .ParamModule import ParamModule
from .QGRFOptimizer import QGRFOptimizer
from .QLinear import QLinear


def _p_modules(self: torch.nn.Module) -> Iterable['ParamModule']:
    return (m for m in self.modules() if isinstance(m, ParamModule))


torch.nn.Module.param_modules = _p_modules
