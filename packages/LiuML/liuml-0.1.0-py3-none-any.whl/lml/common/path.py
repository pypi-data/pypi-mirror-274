#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
from pathlib import Path


def increment_dir(dir_path, comment=''):
    # Increments a directory runs/exp1 --> runs/exp2_comment
    n = 0  # number
    dir_path = str(Path(dir_path))  # os-agnostic
    d = sorted(glob.glob(dir_path + '*'))  # directories
    if len(d):
        n = max([int(x[len(dir_path):x.find('_') if '_' in x else None]) for x in d]) + 1  # increment
    return dir_path + str(n) + ('_' + comment if comment else '')
