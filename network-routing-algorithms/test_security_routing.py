import unittest

from security_routing import Clearance, security_route


class SecurityRouteTests(unittest.TestCase):
    def test_open_route(self):
        stations = [Clearance.NONE, Clearance.NONE]
        segments = [(0, 1, 5, Clearance.NONE)]
        self.assertEqual(security_route(stations, segments, 0, 1), 5)

    def test_clearance_available_at_source(self):
        stations = [Clearance.RED, Clearance.NONE]
        segments = [(0, 1, 3, Clearance.RED)]
        self.assertEqual(security_route(stations, segments, 0, 1), 3)

    def test_clearance_change_at_intermediate_station(self):
        stations = [Clearance.RED, Clearance.BLUE, Clearance.NONE]
        segments = [
            (0, 1, 2, Clearance.RED),
            (1, 2, 4, Clearance.BLUE),
        ]
        self.assertEqual(security_route(stations, segments, 0, 2), 6)

    def test_unreachable_destination(self):
        stations = [Clearance.NONE, Clearance.NONE]
        segments = [(0, 1, 2, Clearance.GREEN)]
        self.assertIsNone(security_route(stations, segments, 0, 1))


if __name__ == "__main__":
    unittest.main()

