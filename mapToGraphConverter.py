from collections import deque, namedtuple
import operator
from whiteMap import WhiteMap
from edgeMap import EdgeMap
import graph
from directions import *

Edge = namedtuple('Edge', 'start, end, cost')
EdgeCell = namedtuple("EdgeCell","start,index")

class Cursor:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    
    @property
    def position(self):
        return (self.x,self.y)

    @position.setter
    def position(self, value):
        self.x = value[0]
        self.y = value[1]

    def move(self, direction):
        return Cursor(*tuple(map(operator.add, self.position, direction)), direction)

    def getPrevious(self):
        previous_dir = oppositeDirection(self.direction)
        return self.move(previous_dir)


class MapToGraphConverter:
    def __init__(self, whiteMap):
        self.whiteMap = whiteMap
        self.edgeMap = EdgeMap.fromDimensions(self.whiteMap.x, self.whiteMap.y)
        self.edges = set()

    def startEdge(self, position, direction):
        self.edgeMap[position][direction] = EdgeCell(position,0)

    def endEdge(self, cursor):
        previous_cursor = cursor.getPrevious()
        last_edgecell = self.edgeMap[previous_cursor.position][cursor.direction]

        self.edges.add(Edge(last_edgecell.start, cursor.position, last_edgecell.index+1))

    def continueEdge(self, cursor):
        previous_cursor = cursor.getPrevious()
        previous_cell = self.edgeMap[previous_cursor.position][cursor.direction]
        self.edgeMap[cursor.position][cursor.direction] = EdgeCell(previous_cell[0], previous_cell[1] + 1)


    def convert(self):
        visited = WhiteMap.fromDimensions(self.whiteMap.x, self.whiteMap.y)
        queue = deque()
        queue.appendleft(Cursor(*self.whiteMap.entrance, Direction.Down))
        self.startEdge(self.whiteMap.entrance, Direction.Down)
        while queue:
            cycle = False
            cur = queue[0]
            queue.popleft()
            white_adjacents = []
            if cur.position != self.whiteMap.exit:
                dirs = getDirectionsToCheck(cur.direction)
                for direction in dirs:
                    check = cur.move(direction)
                    if self.whiteMap[check.position]:
                        white_adjacents.append(check)
                        if not visited[check.position]:
                            queue.appendleft(check)
                        else:
                            cycle = True
            visited[cur.position] = True
            if len(white_adjacents) in [0,2] or white_adjacents[0].direction != cur.direction or cur.position==self.whiteMap.exit:
                self.endEdge(cur)
                for check in white_adjacents:
                    self.startEdge(cur.position, check.direction)
            else:
                if cur.position != self.whiteMap.entrance:
                    self.continueEdge(cur)
                if cycle:
                    print(cur.position)
                    self.endEdge(white_adjacents[0])


    def export(self):
        r = graph.Graph(self.edges)
        return r