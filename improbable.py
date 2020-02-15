"""
Hierarchy stuff:
1) Road types (urban, motorway...)
2) Area types (park, suburban, ...)
...
Building it:
1) Extensible, modules ?
2) Changeability (adding one node and connecting to others) ?
3) Parametric (ordered, chaotic.. different types/styles/scenarios)
4) Use machine learning...
5) Grid of nodes then make edges, (remove unused nodes?), -> lots of space?
6) Generate nodes as you go from one or more starting point (how to keep track if there's a neighbor edge to connect to?)
7) Just generate without coming back (maze-like structure)
8) Discrete points, straight lines then use math functions (e.g. vector fields) to "warp" roads (may cause a lot of bends)

Other parameters... max_nodes?, max_size?, 

What is a node: "Each node in your graph should be associated with a location in three-dimensional space"
-> What is a location: intersection, point of interest...
-> Graphic representation (edge is not necessarily a straight line!)

"""
from collections import namedtuple
from random import randint, random

node = namedtuple('node', 'x y z')

def print_output(nodes, edges):
    for key, value in nodes.items():
        print(f'{value.x}, {value.y}, {value.z}')

    for key, value in edges.items():
        print(f'{value[0]}, {value[1]}')

edges = {}
nodes = {}
nodes[0] = node(2, 3.1, 1.2)
nodes[1] = node(3.5, 2.6, 10.1)
nodes[2] = node(4.1, 3.4, 7.44)
edges[0] = (0, 1)
edges[1] = (1, 2)

print_output(nodes, edges)



from abc import ABC, abstractmethod
from math import radians, cos, sin

class NetworkGenerator(ABC):
    """ Not a Python "generator"
    """
    E = {} # Edges
    N = {} # Nodes
    _nodes_count = 0 # Use nodes count as node ID for simplicity
    _edges_count = 0

    @abstractmethod
    def generate(self) -> (dict, dict):
        # Do something to 
        return (self.E, self.N)

    def add_node(self, node:node) -> None:
        self.N[self._nodes_count] = node
        self._nodes_count += 1

    def connect_nodes(self, IDnode1:int, IDnode2:int) -> None:
        self.E[self._edges_count] = (IDnode1, IDnode2)
        self._edges_count += 1


class FractalNetwork(NetworkGenerator):
    """
    Fractal network generates branches of main branch and sub branches.
    Intersections are not treated as nodes.
    """
    params = namedtuple('FractalGenParams', 'starting_point, max_length, base_angle, angle_deviation, max_recursion')

    def __init__(self):
        self.params.starting_point = node(0,0,0)
        self.params.max_length = 1
        self.params.base_angle = 90
        self.params.angle_deviation = 0
        self.params.max_recursion = 1

    def set_params(self, params: FractalGenParams) -> None:
        self.params = params

    def generate_roads(self) -> (dict, dict):
        
        def recursive_generation(params: FractalGenParams, direction_angle: int=0) -> None:
            self.add_node(params.starting_point)
            
            n_branches = randint(1, 3)
            p1 = params.starting_point

            for branch in range(n_branches):
                new_angle = randint(params.base_angle - params.angle_deviation, params.base_angle + params.angle_deviation)
                new_length = params.max_length*random()

                branch_point = node(p1.x + new_length*cos(new_angle), p1.y + new_length*sin(new_angle), 0)
                
                ID1 = self._nodes_count
                self.add_node(branch_point)
                ID2 = self._nodes_count

                self.connect_nodes(ID1, ID2)



        return (self.E, self.N)



gen = FractalNetwork()

