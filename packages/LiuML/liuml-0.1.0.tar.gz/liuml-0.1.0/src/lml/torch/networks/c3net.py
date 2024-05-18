#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : c3net
@Author: Yingping Li
@Time  : 2022/12/5 16:02
@Desc  : YOLOv5 v6.0 backbone re-impl version
"""
import torch
import torch.nn as nn

class BasicConv2dBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=1, stride=1, padding=None, dilation=1, group=1, **kwargs):
        super(BasicConv2dBlock, self).__init__()
        self.conv = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding if padding is not None else self._auto_same_padding(kernel_size, dilation),
            dilation=dilation,
            group=group,
            bias=False,
            **kwargs
        )
        self.kwargs = kwargs
        self.bn = nn.BatchNorm2d(num_features=out_channels, eps=0.001, momentum=0.01)
        self.act = nn.ReLU(inplace=True)
        self._init_weights()

    @staticmethod
    def _auto_same_padding(kernel_size, dilation):
        kernel_size = kernel_size if dilation == 1 else (dilation * (kernel_size - 1) + 1)
        padding = (kernel_size - 1) // 2
        return padding

    def forward(self, x):
        return self.act(self.bn(self.conv(x)))

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight.data, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()


class SiLUConv2dBlock(BasicConv2dBlock):
    def __init__(self, in_channels, out_channels, *args, **kwargs):
        super(SiLUConv2dBlock, self).__init__(in_channels, out_channels, *args, **kwargs)
        self.act = nn.SiLU(inplace=True)


class StandardBottleneck(nn.Module):
    def __init__(self, in_channels, out_channels, shortcut=True, hidden_channels=None):
        super(StandardBottleneck, self).__init__()
        hidden_channels = hidden_channels or out_channels // 2
        self.cv1 = SiLUConv2dBlock(in_channels=in_channels, out_channels=hidden_channels, kernel_size=1)
        self.cv2 = SiLUConv2dBlock(in_channels=hidden_channels, out_channels=out_channels, kernel_size=3, padding=1)
        self.shortcut = shortcut and in_channels == out_channels

    def forward(self, x):
        return x + self.cv2(self.cv1(x)) if self.shortcut else self.cv2(self.cv1(x))


class StandardC3Block(nn.Module):
    def __init__(self, in_channels, out_channels, depth=1, shortcut=True, hidden_channels=None):
        super(StandardC3Block, self).__init__()
        hidden_channels = hidden_channels or out_channels // 2
        self.cv1 = SiLUConv2dBlock(in_channels=in_channels, out_channels=hidden_channels, kernel_size=1)  # Input Conv
        self.cv2 = SiLUConv2dBlock(in_channels=in_channels, out_channels=hidden_channels,
                                   kernel_size=1)  # Shortcut Conv
        self.cv3 = SiLUConv2dBlock(in_channels=hidden_channels * 2, out_channels=out_channels,
                                   kernel_size=1)  # Output Conv
        self.m = nn.Sequential(
            *(StandardBottleneck(in_channels=hidden_channels, out_channels=hidden_channels, shortcut=shortcut,
                                 hidden_channels=hidden_channels) for _ in range(depth)))

    def forward(self, x):
        return self.cv3(torch.cat((self.m(self.cv1(x)), self.cv2(x)), dim=1))


class FastSPPBlock(nn.Module):
    def __init__(self, in_channels, out_channels, hidden_channels=None):
        super(FastSPPBlock, self).__init__()
        hidden_channels = hidden_channels or out_channels // 2
        self.cv1 = SiLUConv2dBlock(in_channels=in_channels, out_channels=hidden_channels, kernel_size=1)
        self.cv2 = SiLUConv2dBlock(in_channels=hidden_channels * 4, out_channels=out_channels, kernel_size=1)
        self.mp = nn.MaxPool2d(kernel_size=5, stride=1, padding=2)

    def forward(self, x):
        out = [self.cv1(x)]
        for _ in range(3):
            out.append(self.mp(out[-1]))
        return self.cv2(torch.cat(out, dim=1))


class PartialConcat(nn.Module):
    def __init__(self, acquire_layer):
        super(PartialConcat, self).__init__()
        self.acquire_layer = acquire_layer

    def forward(self, x, feats):
        return torch.cat((x, feats[self.acquire_layer]), dim=1)


@BACKBONES.register_module()
class C3Net(nn.Sequential):
    base_depth = (3, 6, 9, 3, 3, 3, 3, 3,)
    base_channel = (64, 128, 128, 256, 256, 512, 512, 1024, 1024, 1024, 512, 512, 256, 256, 256, 512, 512, 1024,)

    def __init__(self,
                 mode='s',
                 out_indices=(17, 20, 23),
                 frozen_stage=-1,
                 init_cfg=dict({})):
        super(C3Net, self).__init__(init_cfg=init_cfg)
        self.out_indices = out_indices
        depth, channel = self._apply_factor(mode=mode)
        self.append(SiLUConv2dBlock(in_channels=3, out_channels=channel[0], kernel_size=6, stride=2, padding=2))
        self.append(
            SiLUConv2dBlock(in_channels=channel[0], out_channels=channel[1], kernel_size=3, stride=2))
        self.append(StandardC3Block(in_channels=channel[1], out_channels=channel[2], depth=depth[0]))
        self.append(
            SiLUConv2dBlock(in_channels=channel[2], out_channels=channel[3], kernel_size=3, stride=2))
        self.append(StandardC3Block(in_channels=channel[3], out_channels=channel[4], depth=depth[1]))
        self.append(
            SiLUConv2dBlock(in_channels=channel[4], out_channels=channel[5], kernel_size=3, stride=2))
        self.append(StandardC3Block(in_channels=channel[5], out_channels=channel[6], depth=depth[2]))
        self.append(
            SiLUConv2dBlock(in_channels=channel[6], out_channels=channel[7], kernel_size=3, stride=2))
        self.append(StandardC3Block(in_channels=channel[7], out_channels=channel[8], depth=depth[3]))
        self.append(FastSPPBlock(in_channels=channel[8], out_channels=channel[9]))
        self.append(SiLUConv2dBlock(in_channels=channel[9], out_channels=channel[10], kernel_size=1))
        self.append(nn.UpsamplingNearest2d(scale_factor=2))
        self.append(PartialConcat(acquire_layer=6))
        self.append(
            StandardC3Block(in_channels=channel[10] * 2, out_channels=channel[11], depth=depth[4], shortcut=False))
        self.append(SiLUConv2dBlock(in_channels=channel[11], out_channels=channel[12], kernel_size=1))
        self.append(nn.UpsamplingNearest2d(scale_factor=2))
        self.append(PartialConcat(acquire_layer=4))
        self.append(
            StandardC3Block(in_channels=channel[12] * 2, out_channels=channel[13], depth=depth[5], shortcut=False))
        self.append(
            SiLUConv2dBlock(in_channels=channel[13], out_channels=channel[14], kernel_size=3, stride=2))
        self.append(PartialConcat(acquire_layer=14))
        self.append(
            StandardC3Block(in_channels=channel[14] * 2, out_channels=channel[15], depth=depth[6], shortcut=False))
        self.append(
            SiLUConv2dBlock(in_channels=channel[15], out_channels=channel[16], kernel_size=3, stride=2))
        self.append(PartialConcat(acquire_layer=10))
        self.append(
            StandardC3Block(in_channels=channel[16] * 2, out_channels=channel[17], depth=depth[7], shortcut=False))

        self.frozen_stage = frozen_stage
        self._freeze_layers()

    def _apply_factor(self, mode):
        depth_factor = dict(n=1, s=1, m=2, l=3, x=4)
        channel_factor = dict(n=1, s=2, m=3, l=4, x=5)
        depth = tuple(map(lambda x: x * depth_factor.get(mode) // 3, self.base_depth))
        channel = tuple(map(lambda x: x * channel_factor.get(mode) // 4, self.base_channel))
        return depth, channel

    def _freeze_layers(self):
        for idx, layer in enumerate(self):
            if idx < self.frozen_stage + 1:
                layer.eval()
                for param in layer.parameters():
                    param.requires_grad = False

    def forward(self, x):
        outs = []
        for layer in self:
            if not isinstance(layer, PartialConcat):
                outs.append(layer(outs[-1] if len(outs) != 0 else x))
            else:
                outs.append(layer(outs[-1], outs))
        return tuple(outs[idx] for idx in self.out_indices)
