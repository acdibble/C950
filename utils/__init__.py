from typing import Match
import re

dirs = {'north': 'N', 'south': 'S', 'east': 'E', 'west': 'W', '\n': ' '}


def replace(m: Match[str]) -> str:
    return dirs[m.group(0).lower()]


def normalize_address(address: str) -> str:
    return re.sub(r'(?i)(north|south|east|west|\n)', replace, address.strip())


def minutes_to_clock(minutes: float) -> str:
    return f'{int(minutes / 60)}:{(int(minutes) % 60):02}'
