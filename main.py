from app import start_app
from wgups.package import Package
from datastructures.hashmap import HashMap
from wgups.schedule import schedule_delivery


package_map = HashMap[str, Package]()
packages, trucks = schedule_delivery()
for p in packages:
    package_map.put(str(p.id), p)

start_app(package_map, trucks)
