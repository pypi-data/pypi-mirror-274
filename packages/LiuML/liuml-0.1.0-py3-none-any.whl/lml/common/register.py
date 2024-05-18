#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import Optional


class Register(dict):
    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self._dict = {}

    def register(self, name=None):
        def default(target):
            key, value = target.__name__ if name is None else name, target
            assert name not in self._dict, f"Object named {name} has already exist."
            self._dict[key] = value
            return value

        return default

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def get(self, name: str, default: object = None) -> Optional[object]:
        ret = self._dict.get(name, default)
        if ret is None and default is None:
            raise KeyError(f"No object named '{name}' found in registry!")
        return ret
