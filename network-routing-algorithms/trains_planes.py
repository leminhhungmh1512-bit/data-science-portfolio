"""Time-dependent rail connectivity using Union-Find."""


class UnionFind:
    """Disjoint-set structure with path compression and union by rank."""

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def add(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0

    def find(self, item):
        self.add(item)
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first, second):
        first_root = self.find(first)
        second_root = self.find(second)

        if first_root == second_root:
            return
        if self.rank[first_root] < self.rank[second_root]:
            self.parent[first_root] = second_root
        elif self.rank[first_root] > self.rank[second_root]:
            self.parent[second_root] = first_root
        else:
            self.parent[second_root] = first_root
            self.rank[first_root] += 1


def replaceable_flights(train_connections, flights):
    """Return flights replaceable by rail on their scheduled date.

    Args:
        train_connections: Iterable of ``(opening_date, city_a, city_b)``.
        flights: Iterable of ``(flight_code, date, departure, arrival)``.

    Returns:
        Flights whose cities are connected by rail on or before the flight date,
        ordered by flight date.
    """

    trains_by_date = sorted(train_connections)
    flights_by_date = sorted(flights, key=lambda flight: flight[1])

    network = UnionFind()
    result = []
    train_index = 0

    for flight in flights_by_date:
        _, flight_date, departure, arrival = flight

        while (
            train_index < len(trains_by_date)
            and trains_by_date[train_index][0] <= flight_date
        ):
            _, city_a, city_b = trains_by_date[train_index]
            network.union(city_a, city_b)
            train_index += 1

        if network.find(departure) == network.find(arrival):
            result.append(flight)

    return result
