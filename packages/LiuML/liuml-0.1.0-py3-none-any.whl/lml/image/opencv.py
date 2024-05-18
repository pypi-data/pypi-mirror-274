#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path as op

import cv2
import numpy as np


def cv2Imread(path, mode=cv2.IMREAD_COLOR):
    """

    Args:
        path: Image Path
        mode: cv2.IMREAD_COLOR -> Load in RGB Mode (Default); cv2.IMREAD_UNCHANGED -> Load in RGBA Mode; cv2.IMREAD_GRAYSCALE -> Load in Gray Mode;

    Returns: Image object in OpenCV

    Desc: A imread wrapper for opencv which support path containing chinese character.

    """
    # cv2.IMREAD_COLOR rgb cv2.IMREAD_GRAYSCALE gray cv2.IMREAD_UNCHANGED rgba
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), mode)
    return image


def cv2Imwrite(path, image):
    cv2.imencode(op.splitext(path)[-1], image)[1].tofile(path)
