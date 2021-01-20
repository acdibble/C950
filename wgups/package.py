from __future__ import annotations
from enum import Enum, auto
import re
from typing import Optional, TYPE_CHECKING
import utils

if TYPE_CHECKING:
    from wgups.truck import Truck

EOD = 24 * 60


class Package:
    class Status(Enum):
        AT_HUB = auto()
        EN_ROUTE = auto()
        DELIVERED = auto()

    @staticmethod
    def parse_time(time: str) -> int:
        if time == 'EOD':
            return EOD

        hours, minutes, meridiem = re.search(
            r'(?i)(\d?\d):(\d\d) ([ap]m)', time).groups()
        offset = 0 if meridiem.lower() == 'am' else 12
        return ((int(hours) + offset) * 60) + int(minutes)

    __required_truck: Optional[int] = None
    wrong_address = False
    __available_at = 8 * 60
    dependencies: set[Package]
    dependent_packages: set[int]
    time_delivered: float = 0

    def __init__(self, id: str, address: str, city: str, state: str, zipcode: str, deadline: str, mass: str, notes: str):
        self.dependent_packages = set[int]()
        self.dependencies = set[Package]()
        self.id = int(id)
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = self.parse_time(deadline)
        self.mass = int(mass)
        self.status = self.Status.AT_HUB
        self.parse_note(notes)
        self.__delivery_address = utils.normalize_address(
            f'{self.address} ({self.zipcode})')

    def __str__(self) -> str:
        deadline = f'{int(self.deadline / 60)}:{int(self.deadline) % 60}'
        return f'id: {self.id}, address: {self.address}, status: {self.status}, deadline: {deadline}'

    def get_address(self) -> str:
        return self.__delivery_address

    def is_priority(self, time: int) -> bool:
        return self.deadline < EOD and self.__is_at_hub() and self.__available_at <= time

    def is_available(self, truck: Truck, exclude: set[Package] = set()) -> bool:
        deps_available = True
        exclude.add(self)
        for deps in [d for d in self.dependencies if not d in exclude]:
            deps_available = deps.is_available(truck, exclude)

        return (deps_available and self.__is_at_hub() and self.__available_at <= truck.get_time()
                and (self.__required_truck == None or self.__required_truck == truck.number))

    def parse_note(self, notes: str) -> None:
        if len(notes) == 0:
            pass
        elif match := re.search(r'\d?\d:\d\d [ap]m', notes):
            self.__available_at = self.parse_time(match.group(0))
        elif match := re.search(r'truck (\d)', notes):
            self.__required_truck = int(match.group(1))
        elif 'delivered with' in notes:
            self.dependent_packages = set[int](
                map(int, re.findall(r'\d+', notes)))
        else:
            self.address = None
            self.city = None
            self.state = None
            self.zipcode = None
            self.__delivery_address = ''
            self.__available_at = self.parse_time('10:20 am')

    def set_en_route(self) -> None:
        self.status = self.Status.EN_ROUTE

    def set_delivered(self, time: float) -> None:
        self.status = self.Status.DELIVERED
        self.time_delivered = time

    def is_delivered(self) -> bool:
        return self.status == self.Status.DELIVERED

    def __is_at_hub(self) -> bool:
        return self.status == self.Status.AT_HUB

    def has_dependencies(self) -> bool:
        return len(self.dependent_packages) != 0
