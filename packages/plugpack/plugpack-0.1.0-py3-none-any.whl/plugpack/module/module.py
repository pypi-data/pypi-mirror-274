# -*- coding: utf-8 -*-

from types import ModuleType
from typing import Union

from plugpack.module.mixin.async_open import ModuleAsyncOpen
from plugpack.module.mixin.doc import ModuleDoc
from plugpack.module.mixin.logger import ModuleLogger
from plugpack.module.mixin.open import ModuleOpen
from plugpack.module.mixin.version import ModuleVersion


class Module(
    ModuleAsyncOpen,
    ModuleDoc,
    ModuleLogger,
    ModuleOpen,
    ModuleVersion,
):
    def __init__(self, module: Union[str, ModuleType], isolate=False, *args, **kwargs):
        if isinstance(module, str):
            self._module = self.import_module(module, isolate=isolate)
        else:
            self._module = module
        self._args = args
        self._kwargs = kwargs

    def open(self) -> None:
        self.on_open(*self._args, **self._kwargs)

    def close(self) -> None:
        self.on_close()

    async def async_open(self) -> None:
        await self.on_async_open(*self._args, **self._kwargs)

    async def async_close(self) -> None:
        await self.on_async_close()
