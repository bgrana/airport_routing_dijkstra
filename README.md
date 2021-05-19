# Airport routing with Dijkstra

For this test, I am tasked to find the shortest route between two airports given a series of connections between them. The project is implemented using `Python 3.7`.

## Dependencies

The only dependency of the project is `Python 3.7` as all other libraries used such as `os`, `sys` and `unittest` are included with base Python. For this reason a virtual environment was not included and the project can be run directly.

The main file of the project can be run with the following terminal command from the root of the project:

```
python3 airport_travel.py ORIGIN DESTINATION
```

Where ORIGIN and DESTINATION are two of the airports included in the test specification document.

## Algorithm Analysis

This project is a clear use case for Dijkstra's Shortest Path algorithm. This algortihm finds the shortest path between 2 nodes (airports) through a series of edges (connections between them provided in the test specification), taking the weight of the edges (time from one airport to another) into account.

Dijkstra's Shortest Path algorithm has an average time complexity of O(E+V<sup>2</sup>). Where E are the edges (connections) and V are the vertices (Nodes). By using a priority queue (or in this case sorting by distance) when selecting the next node to visit in order to visit the one with the minimum distance known we can speed up the algorithm to O((E+V)\*logV).

For the implementation of this project it was assumed that the connections between airports in the test specification are unidirectional (Connection from airport A to B does not imply a connection from B to A unless specified). This makes the graph of the connections directed.

In case we wanted to assume the connections are bidirectional, the algorithm would work just as well and the only changes needed would be to the adjacency list used to represent the graph in order to represent this bidirectionality.

## Unit Tests

A suite of unit tests was developed for testing the basic functionality of the code as well as some corner cases. This was done using the Python library `unittest`.

In order to execute the tests, the following terminal command must be executed (in this case, from the project's root directory):

```
python3 test/test_airport_travel.py
```
