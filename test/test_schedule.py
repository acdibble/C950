import unittest
import re
import json
from wgups.schedule import schedule_delivery


def strip_color_codes(string: str) -> str:
    return re.sub(r'\[\d+?m', '', string)


class TestSchedule(unittest.TestCase):
    def test_schedule(self):
        packages, trucks = schedule_delivery()
        trucks.sort(key=lambda t: t.number)
        truck1, truck2 = trucks
        self.assertEqual(round(truck1.miles_traveled, 1), 74.3)
        self.assertEqual(round(truck2.miles_traveled, 1), 72.9)

        for time in [n * 60 for n in range(8, 13)]:
            with open(f'test/packages/{time}.json', 'r') as f:
                data = json.loads(f.read())
                for pkg in packages:
                    self.assertEqual(
                        data[str(pkg.id)], strip_color_codes(pkg.info(time)))

        for pkg in packages:
            if pkg._Package__required_truck is not None:
                self.assertEqual(pkg._Package__required_truck,
                                 pkg._Package__delivered_by)
            self.assertLessEqual(pkg.delivered_at, pkg.deadline)
            self.assertLessEqual(
                pkg._Package__available_at, pkg._Package__loaded_at)
