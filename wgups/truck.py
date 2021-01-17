from wgups.package import Package


class Truck:
    __number = 0

    @staticmethod
    def get_number() -> int:
        Truck.__number += 1
        return Truck.__number

    miles_traveled = 0
    packages: list[Package] = []

    def __init__(self) -> None:
        self.number = self.get_number()

    def load_package(self, package: Package) -> None:
        package.set_en_route()
        self.packages.append(package)

    def capacity(self) -> int:
        return 16 - len(self.packages)
