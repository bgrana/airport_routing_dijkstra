import sys


# Airport adjacency definition
airports = ['DUB', 'CDG', 'ORD', 'LHR', 'NYC', 'BOS', 'BKK', 'LAX', 'LAS', 'SYD']
distances = {
    'DUB': {'LHR': 1, 'CDG': 2, 'ORD': 6},
    'CDG': {'BOS': 6, 'BKK': 9},
    'ORD': {'LAS': 2},
    'LHR': {'NYC': 5, 'BKK': 9},
    'NYC': {'LAS': 3},
    'BOS': {'LAX': 4},
    'BKK': {'SYD': 11},
    'LAX': {'LAS': 2, 'SYD': 13},
    'LAS': {'SYD': 14},
    'SYD': {}
}


def dijkstra(nodes, distances, start):
    """
    dijkstra

    PRE:
    - nodes: List of nodes present in the graph.
    - distances: Dictionary of edges between the nodes and their weights.
    - start: A node from the nodes list from which to calculate distances

    POST:
    Python dictionary with the distances from the start node to every other node in the graph.
    It also includes for every node: the parent node in the route back to the stars, and the
    distance from that parent node. Structure is as follows:

    {
        node1: {
            distance: d,
            parent: p,
            partialDistance: pd
        },
        .
        .
        .
        nodeN: {
            distance: d,
            parent: p,
            partialDistance: pd
        }
    }

    The start node is included in that dictionary with distance = 0 and parent = None

    """


    # Checks
    if not nodes or type(nodes) is not list:
        raise Exception('This dijkstra function requires a list of nodes.')
    if type(distances) is not dict:
        raise Exception('This dijkstra function requires a dictionary of distances.')
    if start not in nodes:
        raise Exception('Start node is not in the node list.')
    
    # Return map with only start node and distance 0 if distance is map is empty
    if start not in distances:
        return {start: {'distance': 0, 'parent': None, 'partialDistance': 0}}

    # These are all the nodes which have not been visited yet
    unvisited = {node: {'distance': None, 'parent': None, 'partialDistance': None} for node in nodes}
    # It will store the shortest distance from one node to another
    visited = {}
    current = start
    # It will store the predecessors of the nodes
    currentDistance = 0
    unvisited[current] = {'distance': currentDistance, 'parent': current}
    # Running the loop until all the nodes have been visited
    while True:
        # iterating through all the unvisited node
        for neighbour, distance in distances[current].items():
            # Iterating through the connected nodes of current_node 
            # and the weight of the edges
            if neighbour not in unvisited: continue

            newDistance = currentDistance + distance
            if unvisited[neighbour]['distance'] is None or unvisited[neighbour]['distance'] > newDistance:
                unvisited[neighbour] = {'distance': newDistance, 'parent': current, 'partialDistance': distance}
        
        # Move the current node to visited and select the next current
        visited[current] = unvisited[current]
        del unvisited[current]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]['distance']]

        # If there are unvisited nodes left and no distance to them it means
        # the rest of the nodes are not connected to the source one so we end.
        if not candidates: break

        next_node = min(candidates, key = lambda x: x[1]['distance'])
        current = next_node[0]
        currentDistance = next_node[1]['distance']
    return visited


def get_route_str(node_map, start, end):
    """
    get_route_str

    PRE:
    - node_map: A Python dictionary result of a call to dijkstra with the same structure.
    - start: The start node.
    - end: The end node.

    POST:
    A string describing the route of the shortest path between start and end as calculated by dijkstra.
    Uses the following format:
    'A -- B (distAB)\nB -- C (distBC)\n'
    """

    # Checks
    if not node_map or type(node_map) is not dict:
        raise Exception('The first argument needs to be a dictionary of nodes.')
    if start not in node_map:
        raise Exception('The origin node is not in the node_map.')
    if end not in node_map:
        raise Exception('The destination node is not in the node_map.')

    route = ''
    current = end
    counter = 1
    while current != start:
        # Avoid infinite loop in case 'parent' chain never reaches the start node
        if counter > len(node_map.keys()):
            raise Exception('start and end nodes are not connected via parent attributes in the node_map provided')
        
        prev = node_map[current]['parent']
        partial_route = '{prev} -- {current} ({partial})\n'.format(prev=prev, current=current, partial=node_map[current]['partialDistance'])
        route = partial_route + route
        current = prev
        counter += 1

    return route


def calculate_time(airport_origin, airport_destination):
    """
    calculate_time

    PRE:
    - airport_origin: airport from which to start the journey.
    - airport_destination: airport in which the journey ends.

    POST:
    Uses dijkstra to calculate distances from the origin and then uses
    get_route_str to get a string with each step of the journey and then
    adds the total time at the end and returns the entire string.
    """

    res = dijkstra(airports, distances, airport_origin)
    if airport_destination not in res:
        return 'No route available from {origin} to {destination}'.format(origin=airport_origin, destination=airport_destination)
    return '{route_str}time: {time}'.format(route_str=get_route_str(res, airport_origin, airport_destination), time=res[airport_destination]['distance'])


if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception('{args} arguments were read but 2 are needed.'.format(args=len(sys.argv)-1))

    airport_origin = sys.argv[1]
    airport_destination = sys.argv[2]
    print(calculate_time(airport_origin, airport_destination))