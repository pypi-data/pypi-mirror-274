# -*- coding: utf-8 -*-

from typing import Final

from plugpack.module.errors import (
    ModuleCallbackAlreadyStateError,
    ModuleCallbackNotReadyStateError,
    ModuleCallbackRuntimeError,
)
from plugpack.module.mixin._base import ModuleBase

ATTR_ON_OPEN: Final[str] = "on_open"
ATTR_ON_CLOSE: Final[str] = "on_close"


class ModuleOpen(ModuleBase):
    _opened: bool

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._opened = False
        return instance

    @property
    def opened(self) -> bool:
        assert isinstance(self._opened, bool)
        return self._opened

    @property
    def has_on_open(self) -> bool:
        return self.has(ATTR_ON_OPEN)

    @property
    def has_on_close(self) -> bool:
        return self.has(ATTR_ON_CLOSE)

    def on_open(self, *args, **kwargs) -> None:
        if self._opened:
            raise ModuleCallbackAlreadyStateError(self.module_name, ATTR_ON_OPEN)

        callback = self.get(ATTR_ON_OPEN)

        try:
            if callback is not None:
                callback(*args, **kwargs)
        except BaseException as e:
            raise ModuleCallbackRuntimeError(self.module_name, ATTR_ON_OPEN) from e
        else:
            self._opened = True

    def on_close(self) -> None:
        if not self._opened:
            raise ModuleCallbackNotReadyStateError(self.module_name, ATTR_ON_CLOSE)

        callback = self.get(ATTR_ON_CLOSE)

        try:
            if callback is not None:
                callback()
        except BaseException as e:
            raise ModuleCallbackRuntimeError(self.module_name, ATTR_ON_CLOSE) from e
        finally:
            self._opened = False
