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

    def empty(self) -> bool:
        return len(self.packages) == 0

    def full(self) -> bool:
        return len(self.packages) == 16\


    def location(self) -> str:
        return 'HUB' if self.empty() else self.packages[-1].get_address()

    def pretty_time(self) -> str:
        time = self.get_time()
        return f'{int(time / 60)}:{int(time) % 60}'

    def deliver(self, graph: Graph) -> None:
        previous = ''
        current = 'HUB'
        while len(self.packages) != 0:
            previous = current
            pkg = self.packages.pop(0)
            current = pkg.get_address()
            self.miles_traveled += graph.get_distance(previous, current)
            pkg.set_delivered(self.get_time())

        self.miles_traveled += graph.get_distance(current, 'HUB')

        print(self.miles_traveled, self.pretty_time())
