from typing import Iterable, Union, cast
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

graph = Graph[Union[Place, str]]()

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


def find_closest(pkgs: Iterable[Package], loc: Union[str, Place]) -> Package:
    shortest_dist = float('inf')
    closest = None
    for p in pkgs:
        dist = graph.distance_between(p.address, loc)
        if dist < shortest_dist:
            shortest_dist = dist
            closest = p

    return cast(Package, closest)


all_trucks = [Truck(), Truck()]
base_time = 8 * 60


def deliver_packages(trucks: list[Truck]):
    for truck in trucks:
        truck.deliver(graph)
        print(truck.number, truck.location(),
              round(truck.miles_traveled, 1), minutes_to_clock(truck.get_time()))

        for p in all_packages:
            if p.correct_address_available(truck.get_time()):
                p.update_address()


def distribute_packages(packages: Iterable[Package], trucks: list[Truck]):
    for p in packages:
        shortest = float('inf')
        closest = None
        for truck in trucks:
            if p.available_for(truck) and not truck.full():
                dist = graph.distance_between(truck.location(), p.address)
                if dist < shortest:
                    shortest = dist
                    closest = truck

        if closest != None:
            closest.load_package(p)


def load_priority_packages(trucks: list[Truck]):
    priority_packages = [p for p in all_packages if any([p.priority(
        t.get_time()) for t in trucks]) and any([p.available_for(t) for t in trucks])]

    trucks.sort(key=lambda t: t.get_time())
    for truck in trucks:
        while not truck.full() and len(priority_packages) != 0:
            closest = find_closest(priority_packages, truck.location())
            if not closest.at_hub():
                priority_packages.remove(closest)
                continue
            if closest == None:
                break
            deps = closest.dependencies
            for dep in deps:
                deps = deps.union(cast(set[Package], dep.dependencies))
            deps.add(closest)
            if truck.capacity() >= len(deps):
                while len(deps) != 0:
                    pkg = find_closest(deps, truck.location())
                    deps.remove(pkg)
                    if not pkg.at_hub():
                        continue
                    if pkg in priority_packages:
                        priority_packages.remove(pkg)
                    truck.load_package(pkg)
                    for p in [p for p in all_packages if p.address == pkg.address and p.available_for(truck)]:
                        if not truck.full():
                            truck.load_package(p)


def load_packages(trucks: list[Truck]) -> None:
    remaining_packages = [p for p in all_packages if not p.is_delivered()]
    distribute_packages(remaining_packages, trucks)
    deliver_packages(trucks)


while not all_delivered():
    priority_remaining = True
    while priority_remaining:
        load_priority_packages(all_trucks)
        if priority_remaining := any([not truck.empty() for truck in all_trucks]):
            deliver_packages(all_trucks)

    load_packages(all_trucks)


for package in all_packages:
    print(package)
