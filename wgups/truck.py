from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
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
        return (8 * 60) + (self.miles_traveled / 18 * 60)

    def __empty(self) -> bool:
        return len(self.packages) == 0

    def full(self) -> bool:
        return len(self.packages) == 16\


    def location(self) -> str:
        return 'HUB' if self.__empty() else self.packages[-1].address

    def pretty_time(self) -> str:
        time = self.get_time()
        return f'{int(time / 60)}:{int(time) % 60}'

    def deliver(self, graph: Graph) -> None:
        previous = ''
        current = 'HUB'
        while len(self.packages) != 0:
            previous = current
            pkg = self.packages.pop(0)
            current = pkg.address
            self.miles_traveled += graph.distance_between(previous, current)
            pkg.set_delivered(self.get_time())

        self.miles_traveled += graph.distance_between(current, 'HUB')

    def location(self):
        if len(self.packages) != 0:
            return self.packages[-1].address
        else:
            return 'HUB'
