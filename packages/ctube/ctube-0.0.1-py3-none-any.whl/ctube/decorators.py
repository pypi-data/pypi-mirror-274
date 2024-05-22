from signal import signal, SIGINT
from typing import Callable, Any
from ctube.colors import Color, color
from ctube.errors import InvalidSyntax, InvalidIndexSyntax


def handle_main_function(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> None:
        signal(SIGINT, lambda signum, _: exit())
        try:
            func(*args, **kwargs)
        except Exception as error:
            print(color(str(error), Color.RED))
            raise
        exit()
    return inner


def handle_invalid_syntax(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> None:
        try:
            return func(*args, **kwargs)
        except InvalidSyntax:
            print(color("Invalid syntax", Color.RED))
    return inner


def handle_invalid_index_syntax(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> None:
        try:
            return func(*args, **kwargs)
        except InvalidIndexSyntax:
            print(color("Invalid index syntax", Color.RED))
    return inner


def handle_extraction(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (KeyError, IndexError, TypeError, ValueError):
            pass
    return inner
