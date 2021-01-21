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
    __wrong_address = False
    __available_at = float(8 * 60)
    dependencies: set[Package]
    dependent_packages: set[int]
    time_delivered: float = 0

    def __init__(self, id: str, address: str, city: str, state: str, zipcode: str, deadline: str, mass: str, notes: str):
        self.dependent_packages = set[int]()
        self.dependencies = set[Package]()
        self.id = int(id)
        self.__address = address
        self.__city = city
        self.__state = state
        self.__zipcode = zipcode
        self.__deadline = self.parse_time(deadline)
        self.__mass = int(mass)
        self.__status = self.Status.AT_HUB
        self.__parse_note(notes)
        self.address = utils.normalize_address(
            f'{self.__address} ({self.__zipcode})')

    def __str__(self) -> str:
        deadline = utils.minutes_to_clock(self.__deadline)
        delivered_at = utils.minutes_to_clock(self.time_delivered)
        info = [f'id: {self.id}', f'address: {self.__address}',
                f'status: {self.__status}', f'deadline: {deadline}']
        if self.is_delivered():
            info.append(f'delivered at: {delivered_at}')
            info.append(
                f'delivered on time: {self.is_delivered() and self.time_delivered < self.__deadline}')

        return str.join(', ', info)

    def priority(self, time: float) -> bool:
        return self.__at_hub() and self.__deadline < EOD and self.__available_at <= time

    def available_for(self, truck: Truck, exclude: set[Package] = set()) -> bool:
        if self.__wrong_address:
            return False

        if self.__available_at > truck.get_time():
            return False

        if not self.__at_hub():
            return False

        if self.__required_truck != None and self.__required_truck != truck.number:
            return False

        deps_available = True
        exclude.add(self)
        for deps in [d for d in self.dependencies if not d in exclude]:
            deps_available = deps.available_for(truck, exclude)

        return deps_available

    def __parse_note(self, notes: str) -> None:
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
            self.__address = None
            self.__city = None
            self.__state = None
            self.__zipcode = None
            self.address = ''
            self.__available_at = self.parse_time('10:20 am')
            self.__wrong_address = True

    def set_en_route(self) -> None:
        self.__status = self.Status.EN_ROUTE

    def set_delivered(self, time: float) -> None:
        self.__status = self.Status.DELIVERED
        self.time_delivered = time

    def is_delivered(self) -> bool:
        return self.__status == self.Status.DELIVERED

    def __at_hub(self) -> bool:
        return self.__status == self.Status.AT_HUB

    def has_dependencies(self) -> bool:
        return len(self.dependent_packages) != 0

    def correct_address_available(self, time: float):
        return self.__wrong_address and self.__available_at <= time

    def update_address(self):
        self.__wrong_address = False
        self.address = '410 S State St (84111)'
