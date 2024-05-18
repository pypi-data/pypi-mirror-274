#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : basic_conv
@Author: Yingping Li
@Time  : 2022/12/5 16:00
@Desc  :
"""
import torch
import torch.nn as nn


class GeneralConv2dBlock(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        conv_options=None,
        act_type='relu',
        act_options=None,
        norm_options=None
    ):
        super(GeneralConv2dBlock, self).__init__()

        self.conv_options = dict(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=1,
            stride=1,
            padding=None,
            dilation=1,
            group=1,
            bias=False
        )
        if conv_options is not None:
            self.conv_options |= conv_options
        if self.conv_options['padding'] is None:
            self.conv_options['padding'] = self._auto_same_padding(self.conv_options['kernel_size'],
                                                                   self.conv_options['dilation'])
        self.conv = nn.Conv2d(**conv_options)

        self.norm_options = dict(num_features=out_channels)
        if norm_options is not None:
            self.norm_options |= norm_options
        self.bn = nn.BatchNorm2d(**norm_options)

        self.act_options = dict(inplace=True)
        if act_options is not None:
            self.act_options |= act_options
        self.act = self._get_activation(act_type, **act_options)

        self._init_weights()

    @staticmethod
    def _auto_same_padding(kernel_size, dilation):
        kernel_size = kernel_size if dilation == 1 else (dilation * (kernel_size - 1) + 1)
        padding = (kernel_size - 1) // 2
        return padding

    @staticmethod
    def _get_activation(act_type, **kwargs):
        _default = {
            'relu': nn.ReLU,
            'leaky_relu': nn.LeakyReLU,
            'silu': nn.SiLU,
            'hardswish': nn.Hardswish,
        }
        return _default.get(act_type)(**kwargs)

    def _fuse_conv_and_bn(self):
        # Init target conv module
        _conv = nn.Conv2d(**self.conv_options).requires_grad_(False).to(self.conv.device)

        # Acquire parameters and calculate target parameters
        mu, sigma2, eps = self.bn.running_mean, self.bn.running_var, self.bn.eps
        gamma, beta = self.bn.weight, self.bn.bias
        weight = self.conv.weight
        _conv_weight = torch.mm(torch.diag(gamma.div(torch.sqrt(sigma2 + eps))), weight)
        _conv_bias = beta - gamma.mul(mu).div(torch.sqrt(sigma2 + eps))

        # Copy target parameters to target conv module
        _conv.weight.copy_(_conv_weight.view(_conv.weight.shape))
        _conv.bias.copy_(_conv.bias)

        # Modify meta-info of this module
        self.conv = _conv
        delattr(self, 'bn')
        self.forward = self._forward_fuse_bn

    def _forward_fuse_bn(self, x):
        return self.act(self.conv(x))

    def forward(self, x):
        return self.act(self.bn(self.conv(x)))

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight.data, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()


class GeneralRepConv2dBlock(nn.Module):
    def __init__(self):
        super().__init__()
        pass


class BNeckBLock(nn.Module):
    """
    Basic block of MobileNet V3 - 'bneck'

    """

    def __init__(self):
        super().__init__()

