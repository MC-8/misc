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

node = namedtuple('node', 'ID x y z')

def print_output(nodes, edges):
    for key, value in nodes.items():
        print(f'{value.x}, {value.y}, {value.z}')

    for key, value in edges.items():
        print(f'{value[0]}, {value[1]}')

edges = {}
nodes = {}
nodes[0] = node(0, 2, 3.1, 1.2)
nodes[1] = node(1, 3.5, 2.6, 10.1)
nodes[2] = node(2, 4.1, 3.4, 7.44)
edges[0] = (0, 1)
edges[1] = (1, 2)

#print_output(nodes, edges)



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

    def print_network(self):
        for key, value in self.N.items():
            print(f'{value.x}, {value.y}, {value.z}')

        for key, value in self.E.items():
            print(f'{value[0]}, {value[1]}')

    def save_network(self):
        with open('net.out', 'w') as fh:
            for key, value in self.N.items():
                fh.writelines(f'{value.x}, {value.y}, {value.z}\n')

            for key, value in self.E.items():
                fh.writelines(f'{value[0]}, {value[1]}\n')

from copy import deepcopy
class FractalNetwork(NetworkGenerator):
    """
    Fractal network generates branches of main branch and sub branches.
    Intersections are not treated as nodes.
    """
    params = {}
    def __init__(self):
        self.params['starting_point'] = node(0,0,0,0)
        self.params['max_length'] = 100
        self.params['base_angle'] = 0
        self.params['angle_deviation'] = 0
        self.params['max_recursion'] = 3
        self.params['scale_factor'] = 0.7
        self.params['branch_factor_range'] = range(0, 2)

    def set_params(self, params: dict) -> None:
        self.params = params

    def generate(self) -> (dict, dict):
        
        
        def recursive_generation(depth:int, params: dict, direction_angle: int=0) -> None:
            if depth==0: return

            
            p1 = params['starting_point']

            for branch in params['branch_factor_range']:
                new_angle = radians(direction_angle) + radians(params['base_angle']) #radians(randint(params['base_angle'] - params['angle_deviation'], params['base_angle'] + params['angle_deviation']))
                new_length = params['max_length'] #*random()

                branch_point = node(self._nodes_count, p1.x + new_length*cos(new_angle), p1.y + new_length*sin(new_angle), 0) # For now don't do Z branches
                self.add_node(branch_point)
                self.connect_nodes(p1.ID, branch_point.ID)
                p1 = branch_point
                
                new_p = deepcopy(params)
                new_p['max_length'] *= new_p['scale_factor']
                new_p['starting_point'] = branch_point

                recursive_generation(depth=depth-1, params=new_p, direction_angle=direction_angle + 45)
                recursive_generation(depth=depth-1, params=new_p, direction_angle=direction_angle - 45)

        starting_direction = 0
        
        self.add_node(self.params['starting_point'])
        recursive_generation(depth = self.params['max_recursion'], params = self.params, direction_angle=starting_direction)
        recursive_generation(depth = self.params['max_recursion'], params = self.params, direction_angle=starting_direction+90)
        recursive_generation(depth = self.params['max_recursion'], params = self.params, direction_angle=starting_direction+180)
        recursive_generation(depth = self.params['max_recursion'], params = self.params, direction_angle=starting_direction-90)

        return (self.E, self.N)



FN = FractalNetwork()
FN.generate()
FN.print_network()
FN.save_network()

