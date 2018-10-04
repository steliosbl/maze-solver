from collections import deque, namedtuple
import operator
from whiteMap import WhiteMap
from graph import Graph
from mapToGraphConverter import MapToGraphConverter

class Direction:
    Left = (-1, 0)
    Up = (0, -1)
    Right = (1, 0)
    Down = (0, 1)

def oppositeDirection(dir):
    if dir == Direction.Left:
        return Direction.Right
    if dir == Direction.Right:
        return Direction.Left
    if dir == Direction.Up:
        return Direction.Down
    if dir == Direction.Down:
        return Direction.Up

def getDirectionsToCheck(dir):
    r = [Direction.Left,Direction.Up,Direction.Right,Direction.Down]
    r.remove(oppositeDirection(dir))
    return r

def directionToNumber(dir):
    return [Direction.Left,Direction.Up,Direction.Right,Direction.Down].index(dir)

class DirectionList:
    def __init__(self, _):
        self._ = _

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self._[directionToNumber(key)]
        else:
            return self._[key]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self._[directionToNumber(key)] = value
        else:
            self._[key] = value

class EdgeMap:
    def __init__(self, _):
        self._ = _
        self.y = len(_)
        self.x = len(_[0])
    
    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self._[key[1]][key[0]]
        else:
            return self._[key]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self._[key[1]][key[0]] = value
        else:
            self._[key] = value

    def fromDimensions(x,y):
        return EdgeMap([[DirectionList([False, False, False, False]) for i in range(x)] for j in range(y)])
    

Edge = Graph.Edge
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


class TraversalConverter(MapToGraphConverter):
    def __init__(self):
        self.edges = set()
        self.nodes = set()

    def useWhiteMap(self, whiteMap):
        self.whiteMap = whiteMap
        self.edgeMap = EdgeMap.fromDimensions(self.whiteMap.x, self.whiteMap.y)

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
        queue.appendleft(Cursor(*self.whiteMap.endpoints[0], Direction.Down))
        self.startEdge(self.whiteMap.endpoints[0], Direction.Down)
        while queue:
            cycle = False
            cur = queue[0]
            queue.popleft()
            white_adjacents = []
            if cur.position != self.whiteMap.endpoints[1]:
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
            if len(white_adjacents) in [0,2] or white_adjacents[0].direction != cur.direction or cur.position==self.whiteMap.endpoints[1]:
                self.endEdge(cur)
                for check in white_adjacents:
                    self.startEdge(cur.position, check.direction)
            else:
                if cur.position != self.whiteMap.endpoints[0]:
                    self.continueEdge(cur)
                if cycle:
                    self.endEdge(white_adjacents[0])


    def exportGraph(self):
        nodes = {i:Graph.Node(i) for e in self.edges for i in e[:2]}
        for edge in self.edges:
            nodes[edge.start].adjacents.append(nodes[edge.end])
            nodes[edge.end].adjacents.append(nodes[edge.start])
        r = Graph(nodes.values(), self.edges)
        return r
