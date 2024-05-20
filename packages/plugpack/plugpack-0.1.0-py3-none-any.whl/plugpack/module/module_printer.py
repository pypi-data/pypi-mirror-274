# -*- coding: utf-8 -*-

from io import StringIO
from sys import stderr
from typing import Callable, List

from plugpack.module.module import Module
from plugpack.package.package_utils import filter_module_names


def _printable_module_information(
    module_names: List[str],
    module_prefix: str,
    with_version=False,
    with_doc=False,
    with_apis=False,
) -> str:
    buffer = StringIO()

    for module_name in module_names:
        module = Module(module_prefix + module_name, isolate=True)
        version = module.version
        doc = module.doc

        buffer.write(module_name)
        if with_version and version:
            buffer.write(f"@{version}")

        if with_apis:
            has_on_open = "O" if module.has_on_open else "X"
            has_on_close = "O" if module.has_on_close else "X"
            has_on_async_open = "O" if module.has_on_async_open else "X"
            has_on_async_close = "O" if module.has_on_async_close else "X"
            buffer.write(f" [open={has_on_open}")
            buffer.write(f",async_open={has_on_async_open}")
            buffer.write(f",close={has_on_close}")
            buffer.write(f",async_close={has_on_async_close}]")

        if with_doc and doc:
            buffer.write(" ")
            buffer.write(doc)

        buffer.write("\n")

    return buffer.getvalue().strip()


def find_and_strip_module_prefix(module_prefix: str) -> List[str]:
    modules = filter_module_names(module_prefix)
    module_name_begin = len(module_prefix)
    return list(map(lambda x: x[module_name_begin:].strip(), modules))


def print_modules(
    module_prefix: str,
    verbose=0,
    printer: Callable[..., None] = print,
) -> None:
    module_names: List[str]
    try:
        module_names = find_and_strip_module_prefix(module_prefix)
        module_names = list(filter(lambda x: x, module_names))
    except BaseException as e:
        printer(e, file=stderr)
        return

    with_version = verbose >= 1
    with_doc = verbose >= 2
    with_apis = verbose >= 3

    message = _printable_module_information(
        module_names,
        module_prefix,
        with_version,
        with_doc,
        with_apis,
    )

    args = f"with_version={with_version},with_doc={with_doc},with_apis={with_apis}"
    printer(f"List of modules ({args})")

    if message:
        printer(message)
