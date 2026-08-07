"""Tests for the time-dependent rail connectivity algorithm."""

import unittest
from datetime import date

from trains_planes import UnionFind, replaceable_flights


class TestUnionFind(unittest.TestCase):
    def test_connectivity(self):
        network = UnionFind()
        network.union("Perth", "Fremantle")
        network.union("Fremantle", "Rockingham")

        self.assertEqual(network.find("Perth"), network.find("Rockingham"))
        self.assertNotEqual(network.find("Perth"), network.find("Mandurah"))


class TestReplaceableFlights(unittest.TestCase):
    def test_connections_open_over_time(self):
        trains = [
            (date(2026, 1, 1), "Perth", "Fremantle"),
            (date(2026, 2, 1), "Fremantle", "Rockingham"),
            (date(2026, 3, 1), "Rockingham", "Mandurah"),
        ]
        flights = [
            ("WA101", date(2026, 1, 15), "Perth", "Rockingham"),
            ("WA102", date(2026, 2, 15), "Perth", "Rockingham"),
            ("WA103", date(2026, 2, 20), "Perth", "Mandurah"),
            ("WA104", date(2026, 3, 15), "Perth", "Mandurah"),
        ]

        self.assertEqual(replaceable_flights(trains, flights), [flights[1], flights[3]])

    def test_input_order_does_not_matter(self):
        trains = [
            (date(2026, 6, 1), "A", "B"),
            (date(2026, 5, 1), "B", "C"),
        ]
        flights = [
            ("F2", date(2026, 6, 2), "A", "C"),
            ("F1", date(2026, 5, 2), "A", "C"),
        ]

        self.assertEqual(replaceable_flights(trains, flights), [flights[0]])


if __name__ == "__main__":
    unittest.main()
