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
    def __init__(self, whiteMap):
        self.whiteMap = whiteMap
        self.nodes = set()
        self.edges = defaultdict(set)
        self.distances = {}

    def addNode(self, node):
        self.nodes.add(node)
    
    def addEdge(self, start, end, distance):
        self.edges[start].add(end)
        self.distances[(start,end)] = distance

    def checkCursor(self, cursor):
        wa = self.whiteMap.getWhiteAdjacents(self.whiteMap.getAdjacents(*cursor))
        return isNode(wa)

    def fromWhiteMap(self):
        for y in range(self.whiteMap.y):
            for x in range(self.whiteMap.x):
                if self.whiteMap[x,y]:
                    wa = self.whiteMap.getWhiteAdjacents(self.whiteMap.getAdjacents(x,y))
                    if isNode(wa):
                        self.addNode((x,y))

        dirMap = [[[False, False, False, False] for i in range(self.whiteMap.x)] for j in range(self.whiteMap.y)]

        for node in self.nodes:
            #Left
            if not dirMap[node[1]][node[0]][2]:
                d = 0
                cursor = (node[0], node[1])
                while True:
                    d += 1
                    cursor = (cursor[0]-1, cursor[1])
                    if not self.whiteMap[cursor]:
                        break
                    if self.checkCursor(cursor):
                        self.addEdge(cursor,node,d)
                        dirMap[cursor[1]][cursor[0]][0] = True
                        break
            #Up
            if not dirMap[node[1]][node[0]][3]:
                d = 0
                cursor = (node[0], node[1])
                while True:
                    d += 1
                    cursor = (cursor[0], cursor[1]-1)
                    if cursor[1] < 0 or not self.whiteMap[cursor]:
                        break
                    
                    if self.checkCursor(cursor):
                        self.addEdge(cursor,node,d)
                        dirMap[cursor[1]][cursor[0]][1] = True
                        break
            if not dirMap[node[1]][node[0]][0]:
                #Right
                d = 0
                cursor = (node[0], node[1])
                while True:
                    d += 1
                    cursor = (cursor[0]+1, cursor[1])
                    if not self.whiteMap[cursor]:
                        break
                    if self.checkCursor(cursor):
                        self.addEdge(node,cursor,d)
                        dirMap[cursor[1]][cursor[0]][2] = True
                        break
            if not dirMap[node[1]][node[0]][1]:
                #Down
                d = 0
                cursor = (node[0], node[1])
                while True:
                    d += 1
                    cursor = (cursor[0], cursor[1]+1)
                    if cursor[1] >= self.whiteMap.y or not self.whiteMap[cursor]:
                        break
                    if self.checkCursor(cursor):
                        self.addEdge(node,cursor,d)
                        dirMap[cursor[1]][cursor[0]][3] = True
                        break
