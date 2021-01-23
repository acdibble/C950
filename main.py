from app import start_app
from wgups.package import Package
from datastructures.hashmap import HashMap
from wgups.schedule import schedule_delivery


packages = HashMap[str, Package]()
for p in schedule_delivery():
    packages.put(str(p.id), p)

start_app(packages)
