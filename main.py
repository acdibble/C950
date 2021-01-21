from typing import Union
from utils import minutes_to_clock
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
        for i in range(len(dists)):
            distance = float(dists[i])
            graph.add_edge(place, places[i], distance)


def all_delivered() -> bool:
    return all([p.is_delivered() for p in all_packages])


HUB = 'HUB'


def sort_by_closest(pkgs: list[Package], start: Union[str, Place] = HUB):
    pkgs.sort(key=lambda p: graph.distance_between(start, p.address))
    return pkgs


def find_closest(pkgs: list[Package], loc: Union[str, Place]) -> Package:
    shortest_dist = float('inf')
    closest = pkgs[0]
    for p in pkgs:
        dist = graph.distance_between(p.address, loc)
        if dist < shortest_dist:
            shortest_dist = dist
            closest = p

    return closest


def get_priority_packages(time: int) -> list[Package]:
    priority_packages = set()
    for p in all_packages:
        if p.priority(time):
            priority_packages.add(p)
            for dep in p.dependencies:
                priority_packages.add(dep)
    priority_packages = sort_by_closest(list(priority_packages))

    return priority_packages


trucks = [Truck(), Truck()]
base_time = 8 * 60


def deliver_packages():
    for truck in trucks:
        truck.deliver(graph)
        print(truck.number, truck.location(),
              round(truck.miles_traveled, 1), minutes_to_clock(truck.get_time()))

        for p in all_packages:
            if p.correct_address_available(truck.get_time()):
                p.update_address()


def distribute_packages(packages: list[Package]):
    for p in packages:
        dists = [float('inf'), float('inf')]
        for i in range(2):
            if p.available_for(trucks[i]) and not trucks[i].full():
                dists[i] = graph.distance_between(
                    trucks[i].location(), p.address)
        dist1, dist2 = dists
        truck = 0 if dist1 < dist2 else 1
        trucks[truck].load_package(p)


priority_packages = get_priority_packages(base_time)
while len(priority_packages) != 0:
    distribute_packages(priority_packages)
    priority_packages.clear()

    deliver_packages()
    for truck in trucks:
        priority_packages += [p for p in all_packages if p.priority(
            truck.get_time()) and p.available_for(truck)]

while not all_delivered():
    remaining_packages = [p for p in all_packages if not p.is_delivered()]
    distribute_packages(remaining_packages)
    deliver_packages()

for package in all_packages:
    print(package)
