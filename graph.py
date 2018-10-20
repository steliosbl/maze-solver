from collections import namedtuple

class Graph:
    class Node:
        def __init__(self, position):
            self.position = position
            self.adjacents = [False, False, False, False]
            self.distances = [0,0,0,0]

    Edge = namedtuple('Edge', 'start, end, cost')

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def getEndpoints(self, endpoints):
        for node in self.nodes:
            if node.position == endpoints[0]:
                self.entrance = node
            elif node.position == endpoints[1]:
                self.exit = node

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)
