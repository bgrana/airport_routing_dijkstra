import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import airport_travel as at

nodes = ['A', 'B']
distances = {'A': {'B': 1}, 'B': {'A': 2}}

class AirportTravelTest(unittest.TestCase):

    def test_dijkstra_basic(self):
        res = at.dijkstra(nodes, distances, 'A')
        assert res['B']['distance'] == 1
        assert res['A']['distance'] == 0
    
    def test_dijkstra_check_arguments(self):
        # Empty node list
        self.assertRaises(Exception, at.dijkstra, [], distances, 'A')
        
        # Node list is not a list
        self.assertRaises(Exception, at.dijkstra, 'nodes', distances, 'A')
        
        # Distances dict is not a dict
        self.assertRaises(Exception, at.dijkstra, ['A'], 'distances', 'A')
        
        # Start node is not in node list
        self.assertRaises(Exception, at.dijkstra, nodes, distances, 'C')

    def test_dijkstra_1_node_graph(self):
        node = ['A']
        distance = {'A': {'A': 0}}
        res = at.dijkstra(node, distance, 'A')
        assert res['A']['distance'] == 0
        assert len(res.keys()) == 1        

    def test_dijkstra_empty_distances_map(self):
        res = at.dijkstra(nodes, {}, 'A')
        assert res['A']['distance'] == 0
        assert len(res.keys()) == 1

    def test_dijkstra_node_in_distances_not_in_node_list(self):
        pass

    def test_get_route_str_basic(self):
        node_map = {'A': {'parent': 'A', 'partialDistance': 0, 'distance': 0}, 'B': {'parent': 'A', 'partialDistance': 1, 'distance': 1}}
        start = 'A'
        end = 'B'
        res = at.get_route_str(node_map, start, end)

        assert res == 'A -- B (1)\n'


    def test_get_route_str_1_node_map(self):
        node_map = {'B': {'parent': 'B', 'partialDistance': 0, 'distance': 0}}
        start = 'B'
        end = 'B'
        res = at.get_route_str(node_map, start, end)

        assert res == ''

    def test_get_route_str_check_arguments(self):
        # Start is not in node_map
        self.assertRaises(Exception, at.get_route_str, {'A': {}}, 'C', 'A')

        # End is not in node_map
        self.assertRaises(Exception, at.get_route_str, {'A': {}}, 'A', 'C')

        # Node map is empty
        self.assertRaises(Exception, at.get_route_str, {}, 'A', 'C')

        # Node map is not dict
        self.assertRaises(Exception, at.get_route_str, 'node_map', 'A', 'C')

    def test_get_route_str_parent_not_in_node_map(self):
        node_map = {'A': {'parent': 'A', 'partialDistance': 0, 'distance': 0}, 'B': {'parent': 'C', 'partialDistance': 1, 'distance': 1}}
        self.assertRaises(KeyError, at.get_route_str, node_map, 'A', 'B')

    def test_get_route_str_no_route(self):
        node_map = {'A': {'parent': 'A', 'partialDistance': 0, 'distance': 0}, 'B': {'parent': 'B', 'partialDistance': 1, 'distance': 1}}
        self.assertRaises(Exception, at.get_route_str, node_map, 'A', 'B')

    def test_calculate_time_basic(self):
        res = at.calculate_time('CDG', 'LAS')
        assert res == 'CDG -- BOS (6)\nBOS -- LAX (4)\nLAX -- LAS (2)\ntime: 12'

    def test_calculate_time_no_path_available(self):
        res = at.calculate_time('SYD', 'DUB')
        assert res == 'No route available from SYD to DUB'


if __name__ == "__main__":

    # Run Tests
    unittest.main()