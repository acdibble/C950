from typing import Union
from wgups.truck import Truck
from wgups import Place, Package
from datastructures import Graph
import csv

all_packages: list[Package] = []

with open('packages.csv') as f:
    for row in csv.reader(f, delimiter=';'):
        all_packages.append(Package(*row))

for p in all_packages:
    for dep in p.dependent_packages:
        other = all_packages[dep - 1]
        other.dependencies.add(p)
        other.dependent_packages.add(p.id)
        p.dependencies.add(other)

graph = Graph()

with open('distances.csv') as f:
    places: list[Place] = []

    for name, address, *dists in csv.reader(f, delimiter=';', quotechar='"'):
        place = Place(name, address)
        graph.add_vertex(place)
        places.append(place)
        print(place.address)
        for i in range(len(dists)):
            distance = float(dists[i])
            graph.add_edge(place, places[i], distance)


def all_delivered() -> bool:
    return all([p.is_delivered() for p in all_packages])


HUB = 'HUB'


def sort_by_closest(pkgs: list[Package], start: Union[str, Place] = HUB):
    pkgs.sort(key=lambda p: graph.get_distance(start, p.get_address()))
    return pkgs


def find_closest(pkgs: list[Package], loc: Union[str, Place]) -> Package:
    shortest_dist = float('inf')
    closest = pkgs[0]
    for p in pkgs:
        dist = graph.get_distance(p.get_address(), loc)
        if dist < shortest_dist:
            shortest_dist = dist
            closest = p

    return closest


def get_priority_packages(time: int) -> list[Package]:
    priority_packages = set()
    for p in all_packages:
        if p.is_priority(time):
            priority_packages.add(p)
            for dep in p.dependencies:
                priority_packages.add(dep)
    priority_packages = sort_by_closest(list(priority_packages))

    return priority_packages


def load_truck(truck: Truck, packages: list[Package]) -> None:
    for p in packages:
        if p.is_available(truck):
            package_count = 1 + len(p.dependencies)
            if truck.capacity() >= package_count:
                current = p
                truck.load_package(current)
                packages.remove(current)
                deps = list(p.dependencies)
                while len(deps) != 0:
                    print(len(deps))
                    sort_by_closest(deps, current.get_address())
                    print(deps[0], graph.get_distance(
                        current.get_address(), deps[0].get_address()))
                    current = deps.pop(0)
                    truck.load_package(current)
                    if current in packages:
                        packages.remove(current)


trucks = [Truck(), Truck()]
base_time = 8 * 60
priority_packages = get_priority_packages(base_time)
load_truck(trucks[0], priority_packages)
load_truck(trucks[1], priority_packages)

while not all_delivered():
    for truck in [t for t in trucks if not t.full()]:
        print('truck:', truck.number)
        remaining = list(
            filter(lambda p: p.is_available(truck), all_packages))
        while not truck.full():
            print(truck.packages[-1].get_address())
            pkg = find_closest(remaining, truck.packages[-1].get_address())
            truck.load_package(pkg)
            remaining.remove(pkg)
    for truck in trucks:
        print(len(truck.packages))
        truck.deliver(graph)

    for package in all_packages:
        if not package.is_delivered():
            print(package)
    break
