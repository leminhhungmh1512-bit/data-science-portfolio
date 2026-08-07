"""Shortest-path routing with security-clearance constraints."""

from enum import IntEnum


class Clearance(IntEnum):
    NONE = 0
    RED = 1
    BLUE = 2
    GREEN = 3


class MinHeap:
    """Small binary min-heap implementation used by the route search."""

    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._upheap(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._downheap(0)
        return root

    def is_empty(self):
        return not self.heap

    def _upheap(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent][0] <= self.heap[index][0]:
                break
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent

    def _downheap(self, index):
        size = len(self.heap)
        while 2 * index + 1 < size:
            left = 2 * index + 1
            right = left + 1
            smallest = left
            if right < size and self.heap[right][0] < self.heap[left][0]:
                smallest = right
            if self.heap[index][0] <= self.heap[smallest][0]:
                break
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest


def security_route(stations, segments, source, target):
    """Return the minimum travel time from source to target.

    Args:
        stations: Clearance available at each station, or Clearance.NONE.
        segments: Directed edges as (start, end, time, required_clearance).
        source: Starting station index.
        target: Destination station index.

    Returns:
        Minimum travel time, or None when no valid route exists.
    """

    graph = [[] for _ in stations]
    for start, end, travel_time, required_clearance in segments:
        graph[start].append((end, travel_time, required_clearance))

    clearance_count = len(Clearance)
    infinity = float("inf")
    distance = [[infinity] * clearance_count for _ in stations]
    queue = MinHeap()

    distance[source][Clearance.NONE] = 0
    queue.push((0, source, Clearance.NONE))

    while not queue.is_empty():
        current_distance, station, current_clearance = queue.pop()

        if current_distance > distance[station][current_clearance]:
            continue
        if station == target:
            return current_distance

        available_clearance = stations[station]
        if (
            available_clearance != Clearance.NONE
            and available_clearance != current_clearance
            and current_distance < distance[station][available_clearance]
        ):
            distance[station][available_clearance] = current_distance
            queue.push((current_distance, station, available_clearance))

        for next_station, travel_time, required_clearance in graph[station]:
            if required_clearance not in (Clearance.NONE, current_clearance):
                continue
            candidate_distance = current_distance + travel_time
            if candidate_distance < distance[next_station][current_clearance]:
                distance[next_station][current_clearance] = candidate_distance
                queue.push((candidate_distance, next_station, current_clearance))

    return None

