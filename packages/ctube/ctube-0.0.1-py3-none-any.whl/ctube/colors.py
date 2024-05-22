from enum import Enum


class Color(Enum):
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def color(string: str, color: Color) -> str:
    return f"{color.value}{string}{Color.RESET.value}"
