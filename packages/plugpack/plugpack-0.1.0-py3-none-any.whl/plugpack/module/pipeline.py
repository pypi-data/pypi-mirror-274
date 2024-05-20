# -*- coding: utf-8 -*-

from typing import Final, List

PIPE_SEPARATOR: Final[str] = "!"


def module_pipeline_splitter(*args, separator=PIPE_SEPARATOR) -> List[List[str]]:
    result = list()
    module_and_args: List[str] = list()
    for arg in args:
        if arg == separator:
            result.append(module_and_args)
            module_and_args = list()
        else:
            module_and_args.append(arg)
    if module_and_args:
        result.append(module_and_args)
    return result
