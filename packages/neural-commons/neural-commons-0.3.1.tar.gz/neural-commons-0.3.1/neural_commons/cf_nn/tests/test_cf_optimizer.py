import unittest
import torch
from torch import nn

from neural_commons.cf_nn import CFLinear, CFOptimizer, CFConv2d
from neural_commons.cf_nn.tests.utils import IrregularLoss, InvGaussianLoss
from neural_commons.modules import RndProjection, ArgMax, MAELoss, View
from neural_commons.modules.Plus import Plus


class TestCFOptimizer(unittest.TestCase):
    def test_regression_with_bias(self):
        in_features = 32
        out_features = 24
        batch_size = 200
        ref_m = nn.Sequential(
            nn.Linear(in_features, out_features, bias=False),
            Plus(5),
        )
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=True),
        )
        loss_fn = nn.MSELoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.3)

    def test_regression_without_bias(self):
        in_features = 25
        out_features = 44
        batch_size = 200
        ref_m = nn.Linear(in_features, out_features, bias=False)
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=False),
        )
        loss_fn = nn.MSELoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features,
                                                 num_epochs=1)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.3)

    def test_conv2d_with_bias(self):
        in_channels = 16
        out_channels = 24
        batch_size = 200
        width = height = 8
        in_features = width * height * in_channels
        ref_m = nn.Sequential(
            View(-1, in_channels, height, width),
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            View(-1, out_channels * width * height),
            Plus(-3.0),
        )
        opt_m = nn.Sequential(
            View(-1, in_channels, height, width),
            CFConv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=True),
            View(-1, out_channels * width * height),
        )
        loss_fn = nn.MSELoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.3)

    def test_conv2d_without_bias(self):
        in_channels = 16
        out_channels = 24
        batch_size = 200
        width = height = 8
        in_features = width * height * in_channels
        ref_m = nn.Sequential(
            View(-1, in_channels, height, width),
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            View(-1, out_channels * width * height),
        )
        opt_m = nn.Sequential(
            View(-1, in_channels, height, width),
            CFConv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            View(-1, out_channels * width * height),
        )
        loss_fn = nn.MSELoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.3)

    def test_multi_layer(self):
        in_features = 24
        out_features = 32
        batch_size = 200
        ref_m = nn.Linear(in_features, out_features, bias=False)
        opt_m = nn.Sequential(
            CFLinear(in_features, 128),
            RndProjection(128, out_features),
        )
        loss_fn = nn.MSELoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.3)

    def test_mae_loss(self):
        in_features = 32
        out_features = 24
        batch_size = 500
        ref_m = nn.Linear(in_features, out_features, bias=True)
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=True),
        )
        loss_fn = MAELoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features,
                                                 num_epochs=3)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.5)

    def test_ce_loss(self):
        in_features = 34
        out_features = 25
        batch_size = 100
        ref_m = nn.Sequential(
            nn.Linear(in_features, out_features, bias=True),
            ArgMax(),
        )
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=True),
        )
        loss_fn = nn.CrossEntropyLoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.3)

    def test_inv_gaussian_loss(self):
        in_features = 32
        out_features = 24
        batch_size = 200
        ref_m = nn.Linear(in_features, out_features, bias=True)
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=True),
        )
        loss_fn = InvGaussianLoss()
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features,
                                                 num_epochs=3)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.5)

    def test_irregular_loss(self):
        in_features = 34
        out_features = 30
        batch_size = 200
        ref_m = nn.Linear(in_features, out_features, bias=True)
        opt_m = nn.Sequential(
            CFLinear(in_features, out_features, bias=True),
        )
        loss_fn = IrregularLoss(out_features)
        loss_value_1, loss_value_2 = self._train(ref_m, opt_m, loss_fn, batch_size, in_features,
                                                 num_epochs=3)
        print(f"Initial loss value: {loss_value_1}")
        print(f"Final loss value: {loss_value_2}")
        self.assertLess(loss_value_2, loss_value_1 * 0.8)

    def _train(self, ref_m: nn.Module,
               opt_m: nn.Module, loss_fn: nn.Module, batch_size: int, in_features: int,
               num_epochs: int = 1):
        x = torch.randn((batch_size, in_features))
        label = ref_m(x)
        optimizer = CFOptimizer(opt_m.cf_modules())
        y1 = opt_m(x)
        loss_value_1 = loss_fn(y1, label).item()
        for e in range(num_epochs):
            def _fn() -> torch.Tensor:
                y = opt_m(x)
                _loss = loss_fn(y, label)
                return _loss

            optimizer.enqueue_data(_fn)
            if optimizer.queued_batch_size >= 1:
                optimizer.step()
        pred_y_2 = opt_m(x)
        loss = loss_fn(pred_y_2, label)
        loss_value_2 = torch.mean(loss).item()
        return loss_value_1, loss_value_2,
