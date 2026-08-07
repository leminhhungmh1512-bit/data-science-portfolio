# Network Routing and Connectivity Algorithms

## Overview

This project contains two Python algorithms for evolving transport networks:

1. **Security-constrained routing** finds the minimum travel time through a directed network when route segments may require different security clearances.
2. **Train and plane connectivity** identifies flights that can be replaced by rail as new train connections open over time.

Both solutions use custom data structures and require no third-party packages.

## Security-Constrained Routing

- Represent each search state as `(station, clearance)`.
- Build a directed adjacency list from the route segments.
- Use a custom binary min-heap as the priority queue.
- Apply Dijkstra-style relaxation to travel actions and zero-time clearance changes.
- Return `None` when the destination cannot be reached.

With four fixed clearance states, the time complexity is approximately **O((V + E) log V)**.

## Train and Plane Connectivity

- Process rail openings and scheduled flights in chronological order.
- Use Union-Find to maintain connected components in the rail network.
- Apply path compression and union by rank for efficient connectivity checks.
- Return flights whose departure and arrival cities are rail-connected by the flight date.

Sorting dominates the runtime, giving **O(N log N)** time for `N` rail connections and flights.

## Files

```text
network-routing-algorithms/
├── security_routing.py
├── trains_planes.py
├── test_security_routing.py
└── test_trains_planes.py
```

## Run the Tests

```bash
python -m unittest -v
```

No third-party packages are required.
