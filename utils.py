import os
from typing import Any, Match
import re

dirs = {'north': 'N', 'south': 'S', 'east': 'E', 'west': 'W', '\n': ' '}


def replace(m: Match[str]) -> str:
    return dirs[m.group(0).lower()]


def normalize_address(address: str) -> str:
    return re.sub(r'(?i)(north|south|east|west|\n)', replace, address.strip())


def minutes_to_clock(minutes: float) -> str:
    return f'{int(minutes / 60)}:{(int(minutes) % 60):02}'


def clock_to_minutes(clock: str) -> int:
    hours, minutes = list(map(int, clock.split(':')))
    if 0 <= hours < 24 and 0 <= minutes < 60:
        return hours * 60 + minutes

    raise Exception


def debug(*args) -> None:
    if os.environ.get('DEBUG') == 'true':
        print(*args)


class ANSICodes:
    CLEAR = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

    @staticmethod
    def green(line: Any) -> str:
        return f'{ANSICodes.GREEN}{line}{ANSICodes.CLEAR}'

    @staticmethod
    def cyan(line: Any) -> str:
        return f'{ANSICodes.CYAN}{line}{ANSICodes.CLEAR}'

    @staticmethod
    def blue(line: Any) -> str:
        return f'{ANSICodes.BLUE}{line}{ANSICodes.CLEAR}'

    @staticmethod
    def red(line: Any) -> str:
        return f'{ANSICodes.RED}{line}{ANSICodes.CLEAR}'
