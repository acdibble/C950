import unittest
from datastructures import HashMap


class TestMap(unittest.TestCase):
    def test_put(self):
        m = HashMap[int, int]()
        m.put(1, 2)
        self.assertEqual(
            m._Map__storage,
            [[], [(1, 2)], [], [], [], [], [], [], [], []]
        )
        self.assertEqual(m.size, 1)

        m.put(1, 3)
        self.assertEqual(
            m._Map__storage,
            [[], [(1, 3)], [], [], [], [], [], [], [], []]
        )
        self.assertEqual(m.size, 1)

    def test_get(self):
        m = HashMap[object, object]()
        m.put(1, 2)
        self.assertEqual(m.get(1), 2)
        m.put(1, 3)
        self.assertEqual(m.get(1), 3)
        m.put(21, 3)
        self.assertEqual(m.get(1), 3)
        self.assertEqual(m.get(21), 3)
        m.put(31, 3)
        self.assertEqual(m.get(1), 3)
        self.assertEqual(m.get(21), 3)
        self.assertEqual(m.get(31), 3)
        m.put('key', 'value')
        self.assertEqual(m.get('key'), 'value')
