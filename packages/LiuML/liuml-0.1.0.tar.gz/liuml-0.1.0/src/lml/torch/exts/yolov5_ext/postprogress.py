#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : postprogress
@Author: Yingping Li
@Time  : 2022/12/5 17:24
@Desc  :
"""
import torch

# Enhence YOLOv5 Segementation with Pixel-level NMS
def mask_matrix_nms(masks, scores, classes, iou_threshold: float, eps=1e-7):
    """
    :param boxes: [N, 4]， 此处传进来的框，是经过筛选（NMS之前选取过得分TopK）之后， 在传入之前处理好的；
    :param scores: [N]
    :param iou_threshold: 0.7
    :return:
    """
    idxs = torch.arange(0, scores.shape[0])
    mask_id = classes.expand(scores.shape[0], scores.shape[0])
    label_mask = (mask_id == mask_id.T).float().triu(diagonal=1)
    masks = masks.flatten(1)
    intersection = masks.mm(masks.T)
    area = masks.sum(1).expand_as(intersection)
    union = area + area.T - intersection
    ious = (intersection / union + eps).triu(diagonal=1)
    max_ious = (label_mask * ious).max(0)
    keep = idxs[max_ious[0] < iou_threshold]
    return keep
