from typing import Optional
import torch
from torch import nn, autograd


class ParamModule(nn.Module):
    gradients: Optional[tuple[torch.Tensor, ...]]
    lr: Optional[torch.Tensor]

    def __init__(self, *tensors: torch.Tensor, approx_lr: float = None,
                 alpha: float = 0.3, scale: float = None):
        super().__init__()
        num_tensors = len(tensors)
        if num_tensors == 0:
            raise ValueError("At least one tensor must be provided.")
        for i, t in enumerate(tensors):
            self.register_buffer(f"tensor{i}", t.requires_grad_())
        first_tensor = tensors[0]
        self.num_tensors = num_tensors
        self.gradients = None
        self.lr = None
        self.alpha = alpha
        self.approx_lr_ma = approx_lr or 0.5 * first_tensor.size(0)
        if scale is not None:
            self.scale = scale
        else:
            rms = torch.sqrt(torch.mean(first_tensor.pow(2))).item()
            self.scale = 1.0 if rms == 0 else rms

    def update_approx_lr(self, lr: float):
        self.approx_lr_ma = lr * self.alpha + self.approx_lr_ma * (1 - self.alpha)

    def get_approx_lr(self) -> float:
        return self.approx_lr_ma

    def set_gradient(self, gradients: tuple[torch.Tensor, ...], lr: torch.Tensor):
        self.gradients = gradients
        self.lr = lr

    def clear_gradient(self):
        self.gradients = None
        self.lr = None

    @property
    def tensors(self) -> tuple[torch.Tensor, ...]:
        return tuple(getattr(self, f"tensor{i}") for i in range(self.num_tensors))

    def increment_tensors(self, offsets: tuple[torch.Tensor, ...]):
        for i in range(self.num_tensors):
            attr = f"tensor{i}"
            tensor = getattr(self, attr)
            setattr(self, attr, (tensor + offsets[i]).detach().requires_grad_())

    def grad(self, loss: torch.Tensor) -> tuple[torch.Tensor, ...]:
        return autograd.grad(loss, self.tensors)

    def forward(self) -> tuple[torch.Tensor, ...]:
        if self.gradients is not None:
            lr = self.lr
            gen = (t - g * lr for t, g in zip(self.tensors, self.gradients))
            return tuple(gen)
        else:
            return self.tensors
