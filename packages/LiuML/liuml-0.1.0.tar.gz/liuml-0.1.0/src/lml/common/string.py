#!/usr/bin/python3
# -*- coding: utf-8 -*-
import ctypes
import json
import sys
from enum import Enum
from typing import Optional


class TerminalColor(Enum):
    BLACK = 0
    BLUE = 1
    GREEN = 2
    CYAN = 3
    RED = 4
    PURPLE = 5
    YELLOW = 6
    WHITE = 7
    GRAY = 8
    LIGHT_BLUE = 9
    LIGHT_GREEN = 10
    LIGHT_CYAN = 11
    LIGHT_RED = 12
    LIGHT_PURPLE = 13
    LIGHT_YELLOW = 14
    LIGHT_WHITE = 15


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
STD_COLOR_RESET = TerminalColor.WHITE.value | TerminalColor.BLACK.value << 4


def is_int(
        string: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
) -> bool:
    """
    Check if a string is an integer number
    :param string:
    :param min_value:
    :param max_value:
    :return:
    """
    try:
        if not all(char.isdigit() or char == "-" for char in string):
            return False
        int_value = int(string)
        if min_value is not None and int_value < min_value:
            return False
        if max_value is not None and int_value > max_value:
            return False
        return True
    except ValueError:
        return False


def if_float(
        string: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
) -> bool:
    """
    Check if a string is a float number
    :param string:
    :param min_value:
    :param max_value:
    :return:
    """
    try:
        if "." not in string:
            return False
        float_value = float(string)
        if min_value is not None and float_value < min_value:
            return False
        if max_value is not None and float_value > max_value:
            return False
        return True
    except ValueError:
        return False


def is_json_object(string: str) -> bool:
    """
    Check if a string is a json object
    :param string:
    :return:
    """
    try:
        json_decode = json.loads(string)
        return isinstance(json_decode, dict)
    except json.JSONDecodeError:
        return False


def is_json_array(string: str) -> bool:
    """
    Check if a string is a json array
    :param string:
    :return:
    """
    try:
        json_decode = json.loads(string)
        return isinstance(json_decode, list) and all(isinstance(item, dict) for item in json_decode)
    except json.JSONDecodeError:
        return False


def is_json(string: str) -> bool:
    """
    Check if a string is a json object or json array
    :param string:
    :return:
    """
    return is_json_object(string) or is_json_array(string)


def color_print(*args, fg: Optional[TerminalColor] = None, bg: Optional[TerminalColor] = None, **kwargs) -> None:
    """
    Print text with color on POSIX terminal
    :param fg:
    :param bg:
    :param args:
    :param kwargs:
    :return:
    """
    if sys.platform == "win32":
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        fg: TerminalColor = fg or TerminalColor.WHITE
        bg: TerminalColor = bg or TerminalColor.BLACK
        color = fg.value | bg.value << 4
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    print(*args, **kwargs)
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, STD_COLOR_RESET)


if __name__ == "__main__":
    color_print("Hello, world!", fg=TerminalColor.BLUE, bg=TerminalColor.WHITE)
    print("haha")
