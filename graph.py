from itertools import groupby
from operator import itemgetter
from collections import defaultdict

def getRanges(data):
    ranges = []
    for key, group in groupby(enumerate(data), lambda i: i[0] - i[1]):
        group = list(map(itemgetter(1), group))
        if len(group) > 1:
            ranges.append((group[0], group[-1]))
        else:
            ranges.append(group[0])
    return ranges

def isNode(wa):
    if len(wa) == 2:
        return not (wa[0][0] == wa[1][0] or wa[0][1] == wa[1][1])
    else:
        return True

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)
        self.distances = {}

    def addNode(self, node):
        self.nodes.add(node)
    
    def addEdge(self, start, end, distance):
        self.edges[start].add(end)
        # self.edges[end].append(start)
        self.distances[(start,end)] = distance

    def fromWhiteMap(self, whiteMap):
        for y in range(whiteMap.y):
            for x in range(whiteMap.x):
                if whiteMap[x,y]:
                    wa = whiteMap.getWhiteAdjacents(whiteMap.getAdjacents(x,y))
                    if isNode(wa):
                        self.addNode((x,y))

        for node in self.nodes:
            #Left
            d = 0
            cursor = (node[0], node[1])
            while True:
                d += 1
                cursor = (cursor[0]-1, cursor[1])
                if not whiteMap[cursor]:
                    break
                if cursor in self.nodes:
                    self.addEdge(cursor,node,d)
                    break
            #Up
            d = 0
            cursor = (node[0], node[1])
            while True:
                d += 1
                cursor = (cursor[0], cursor[1]-1)
                if cursor[1] < 0 or not whiteMap[cursor]:
                    break
                if cursor in self.nodes:
                    self.addEdge(cursor,node,d)
                    break
            #Right
            d = 0
            cursor = (node[0], node[1])
            while True:
                d += 1
                cursor = (cursor[0]+1, cursor[1])
                if not whiteMap[cursor]:
                    break
                if cursor in self.nodes:
                    self.addEdge(node,cursor,d)
                    break
            #Down
            d = 0
            cursor = (node[0], node[1])
            while True:
                d += 1
                cursor = (cursor[0], cursor[1]+1)
                if cursor[1] >= whiteMap.y or not whiteMap[cursor]:
                    break
                if cursor in self.nodes:
                    self.addEdge(node,cursor,d)
                    break