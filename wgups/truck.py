from __future__ import annotations
from typing import TYPE_CHECKING, Union
from utils import minutes_to_clock
if TYPE_CHECKING:
    from wgups.place import Place
    from wgups.package import Package
    from datastructures.graph import Graph


class Truck:
    __number = 0

    @staticmethod
    def __get_number() -> int:
        Truck.__number += 1
        return Truck.__number

    miles_traveled: float = 0
    packages: list[Package]
    number: int

    @staticmethod
    def __calc_time(time: float) -> float:
        return (8 * 60) + (time / 18 * 60)

    def __init__(self) -> None:
        self.number = self.__get_number()
        self.packages = []

    def load_package(self, package: Package) -> None:
        if self.capacity() == 0:
            raise Exception

        package.set_en_route()
        self.packages.append(package)

    def capacity(self) -> int:
        return 16 - len(self.packages)

    def get_time(self) -> float:
        return self.__calc_time(self.miles_traveled)

    def empty(self) -> bool:
        return len(self.packages) == 0

    def full(self) -> bool:
        return len(self.packages) == 16

    def location(self) -> str:
        return 'HUB' if self.empty() else self.packages[-1].address

    def pretty_time(self) -> str:
        time = self.get_time()
        return f'{int(time / 60)}:{int(time) % 60}'

    def deliver(self, graph: Graph[Union[Place, str]]) -> None:
        previous = ''
        current = 'HUB'
        for pkg in self.packages:
            previous = current
            current = pkg.address
            self.miles_traveled += graph.distance_between(previous, current)
            pkg.set_delivered(self.get_time())
            info = f'truck {self.number}'
            info += f' delivered package {pkg.id}'
            info += f' at {minutes_to_clock(pkg.time_delivered)}'
            info += f' to address {pkg.address}'
            info += f' after {round(self.miles_traveled, 1)} miles'
            print(info)

        self.packages.clear()
        self.miles_traveled += graph.distance_between(current, 'HUB')
        print(
            f'returned to HUB with {round(self.miles_traveled, 1)} miles on the odo')

    def location(self):
        if len(self.packages) != 0:
            return self.packages[-1].address
        else:
            return 'HUB'

    def predict_time(self, graph: Graph[Union[Place, str]], package: Package) -> bool:
        previous = ''
        current = 'HUB'
        temp_traveled = self.miles_traveled
        for pkg in self.packages:
            previous = current
            current = pkg.address
            temp_traveled += graph.distance_between(previous, current)

        temp_traveled += graph.distance_between(current, package.address)
        return self.__calc_time(temp_traveled) <= package.deadline
