# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction
from typing import Final

from plugpack.module.errors import (
    ModuleCallbackAlreadyStateError,
    ModuleCallbackNotCoroutineError,
    ModuleCallbackNotReadyStateError,
    ModuleCallbackRuntimeError,
)
from plugpack.module.mixin._base import ModuleBase

ATTR_ON_ASYNC_OPEN: Final[str] = "on_async_open"
ATTR_ON_ASYNC_CLOSE: Final[str] = "on_async_close"


class ModuleAsyncOpen(ModuleBase):
    _async_opened: bool

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._async_opened = False
        return instance

    @property
    def async_opened(self) -> bool:
        assert isinstance(self._async_opened, bool)
        return self._async_opened

    @property
    def has_on_async_open(self) -> bool:
        return self.has(ATTR_ON_ASYNC_OPEN)

    @property
    def has_on_async_close(self) -> bool:
        return self.has(ATTR_ON_ASYNC_CLOSE)

    async def on_async_open(self, *args, **kwargs) -> None:
        if self._async_opened:
            raise ModuleCallbackAlreadyStateError(self.module_name, ATTR_ON_ASYNC_OPEN)

        callback = self.get(ATTR_ON_ASYNC_OPEN)

        if callback is not None and not iscoroutinefunction(callback):
            raise ModuleCallbackNotCoroutineError(self.module_name, ATTR_ON_ASYNC_OPEN)

        try:
            if callback is not None:
                await callback(*args, **kwargs)
        except BaseException as e:
            raise ModuleCallbackRuntimeError(
                self.module_name, ATTR_ON_ASYNC_OPEN
            ) from e
        else:
            self._async_opened = True

    async def on_async_close(self) -> None:
        if not self._async_opened:
            raise ModuleCallbackNotReadyStateError(
                self.module_name, ATTR_ON_ASYNC_CLOSE
            )

        callback = self.get(ATTR_ON_ASYNC_CLOSE)

        if callback is not None and not iscoroutinefunction(callback):
            raise ModuleCallbackNotCoroutineError(self.module_name, ATTR_ON_ASYNC_CLOSE)

        try:
            if callback is not None:
                await callback()
        except BaseException as e:
            raise ModuleCallbackRuntimeError(
                self.module_name, ATTR_ON_ASYNC_CLOSE
            ) from e
        finally:
            self._async_opened = False
