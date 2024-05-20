from typing import Iterable

import torch

from .CFModule import CFModule
from .CFLinear import CFLinear
from .CFConv2d import CFConv2d
from .CFOptimizer import CFOptimizer


def _cf_modules(self: torch.nn.Module) -> Iterable['CFModule']:
    return (m for m in self.modules() if isinstance(m, CFModule))


torch.nn.Module.cf_modules = _cf_modules
