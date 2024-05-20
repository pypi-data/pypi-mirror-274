import torch
from torch import nn

from neural_commons.helpers.torch_helper import dims_from
from neural_commons.modules import RndProjection


class InvGaussianLoss(nn.Module):
    def forward(self, pred: torch.Tensor, target: torch.Tensor):
        diff_sq = (pred - target).pow(2)
        mse = torch.mean(diff_sq)
        return 1.0 - torch.exp(-mse * 2)


class IrregularLoss(nn.Module):
    def __init__(self, num_features: int):
        super().__init__()
        self.rp = RndProjection(num_features, 2, seed=3001)

    def forward(self, pred: torch.Tensor, target: torch.Tensor):
        logits = self.rp(target) * 3
        w1 = torch.sigmoid(logits[:, [0]])
        w2 = torch.sigmoid(logits[:, [1]])
        diff_sq = (pred - target).pow(2)
        abs_diff = torch.abs(pred - target)
        dim = dims_from(pred)
        mse = torch.mean(diff_sq, dim=dim)
        loss1 = 1.0 - torch.exp(-mse * w2 * 4)
        loss2 = torch.mean(abs_diff, dim=dim)
        loss = loss1 * w1 + loss2 * (1 - w1)
        return torch.mean(loss)

