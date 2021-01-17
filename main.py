from wgups import Place, Package
from datastructures import Graph
import csv

packages: list[Package] = []

with open('packages.csv') as f:
    for row in csv.reader(f, delimiter=';'):
        packages.append(Package(*row))

for p in [p for p in packages if p.has_dependencies()]:
    print(p.id, p.dependencies)
    for dep in p.dependencies:
        print(dep, packages[dep - 1].id)
        packages[dep - 1].dependencies.add(p.id)
for p in [p for p in packages if p.has_dependencies()]:
    print(p.id, p.dependencies)

graph = Graph()

with open('distances.csv') as f:
    places: list[Place] = []

    for name, address, *dists in csv.reader(f, delimiter=';', quotechar='"'):
        place = Place(name, address)
        graph.add_vertex(place)
        places.append(place)
        print(place.address)
        for i in range(len(dists)):
            if ((distance := float(dists[i])) != 0.0):
                graph.add_edge(place, places[i], distance)


def all_delivered() -> bool:
    return all([p.is_delivered() for p in packages])


HUB = 'HUB'


def get_priority_packages() -> list[Package]:
    priority_packages = set()
    for p in packages:
        if p.is_priority(time):
            priority_packages.add(p)
            for dep in p.dependencies:
                priority_packages.add(packages[dep - 1])
    priority_packages = list(priority_packages)
    priority_packages.sort(
        key=lambda p: graph.get_distance(HUB, p.get_address()))
    return priority_packages


time = 8 * 60
while not all_delivered():
    priority_packages = get_priority_packages()
    for p in priority_packages:
        print(p, graph.get_distance(HUB, p.get_address()))
    break
