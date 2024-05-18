#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging


def get_logger(file=False, filename="tmp.log"):
    log_format = '[%(asctime)s]-[%(filename)s::%(funcName)s::%(lineno)s] %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
    )
    logger = logging.getLogger()
    if file:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
    return logger
