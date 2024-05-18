#!/usr/bin/python3
# -*- coding: utf-8 -*-
import contextlib
import time

from importlib import import_module

import pkg_resources

from lml.common.logger import get_logger


class Timer(contextlib.ContextDecorator):
    def __init__(self):
        self.t = 0.0
        self.record = []
        self.logger = get_logger()

    def __enter__(self):
        self.start = self.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dt = self.time() - self.start
        if len(self.record) > 1:
            self.logger.info(f"Total Running Time: {self.dt}, Average Running Time: {self.dt / len(self.record)}")
        else:
            self.logger.info(f"Running Time: {self.dt}")

    def step(self):
        dt = self.time() - self.start - self.t
        self.t += dt
        self.record.append(dt)
        self.logger.info(
            f"Record-{len(self.record)}: last range interval {dt}, total time {self.t}"
        )

    @staticmethod
    def time():
        return time.time()


class TorchTimer(Timer):
    def __init__(self):
        super().__init__()
        try:
            pkg_resources.require('torch')
            module = import_module('torch')

            def _time():
                module.cuda.synchronize()
                return time.time()

            if module.cuda.is_available():
                self.time = _time
        except pkg_resources.DistributionNotFound:
            pass  # Just a simple Timer()
