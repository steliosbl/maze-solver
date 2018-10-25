from mapToGraphConverter import MapToGraphConverter
from collections import namedtuple
from graph import Graph
Node = Graph.Node
Edge = Graph.Edge

class ScanConverter(MapToGraphConverter):
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def convert(self):
        self.whiteMap._.append([False] * self.whiteMap.x) #Add additional wall to bottom so that scanning final row does not cause crash by trying to find below exit
        upBuffer = [None] * self.whiteMap.x
        upBuffer[self.whiteMap.endpoints[0][0]] = Node(self.whiteMap.endpoints[0])
        for y in range(self.whiteMap.y):
            leftBuffer = None
            previous = False
            next = False
            current = False
            for x in range(1, self.whiteMap.x): #No need to check index 0 since we know it is a wall
                node = None
                previous, current = current, next
                next = self.whiteMap._[y][x]
                x -= 1
                above = self.whiteMap._[y-1][x]
                below = self.whiteMap._[y+1][x]
                if x == 373 and y == 3:
                    print(str(previous)+str(current)+str(next)+str(above)+str(below))
                if current: #All cases other than those below are not nodes, so are not checked
                    if previous:
                        if next: #WWW
                            if above or below:
                                node = Node((x,y))
                                self.nodes.add(node)
                                cost = x-leftBuffer.position[0] +1
                                node.adjacents[0] = leftBuffer
                                node.distances[0] = cost
                                leftBuffer.adjacents[2] = node
                                leftBuffer.distances[2] = cost
                                self.edges.add(Edge(leftBuffer.position, node.position, cost))
                                leftBuffer = node
                                if above:
                                    cost = y-upBuffer[x].position[1] + 1
                                    node.adjacents[1] = upBuffer[x]
                                    node.distances[1] = cost
                                    upBuffer[x].adjacents[3] = node
                                    upBuffer[x].distances[3] = cost
                                    self.edges.add(Edge(upBuffer[x].position, node.position, cost))
                                if below:
                                    upBuffer[x] = node
                        
                        else: #WWB
                            node = Node((x,y))
                            self.nodes.add(node)
                            cost = x-leftBuffer.position[0] +1
                            node.adjacents[0] = leftBuffer
                            node.distances[0] = cost
                            leftBuffer.adjacents[2] = node
                            leftBuffer.distances[2] = cost
                            self.edges.add(Edge(leftBuffer.position, node.position, cost))
                            if above:
                                cost =  y-upBuffer[x].position[1] + 1
                                node.adjacents[1] = upBuffer[x]
                                node.distances[1] = cost
                                upBuffer[x].adjacents[3] = node
                                upBuffer[x].distances[3] = cost
                                self.edges.add(Edge(upBuffer[x].position, node.position, cost))
                            if below:
                                upBuffer[x] = node
                    else:
                        if next: #BWW
                            node = Node((x,y))
                            self.nodes.add(node)
                            leftBuffer = node
                            if above:
                                cost = y-upBuffer[x].position[1] + 1
                                node.adjacents[1] = upBuffer[x]
                                node.distances[1] = cost
                                upBuffer[x].adjacents[3] = node
                                upBuffer[x].distances[3] = cost
                                self.edges.add(Edge(upBuffer[x].position, node.position, cost))
                            if below:
                                upBuffer[x] = node

                        else: #BWB
                            if above != below: #XOR
                                node = Node((x,y))
                                self.nodes.add(node)
                                if above:
                                    cost = y-upBuffer[x].position[1] + 1
                                    node.adjacents[1] = upBuffer[x]
                                    node.distances[1] = cost
                                    upBuffer[x].adjacents[3] = node
                                    upBuffer[x].distances[3] = cost
                                    self.edges.add(Edge(upBuffer[x].position, node.position, cost))
                                if below:
                                    upBuffer[x] = node

    def exportGraph(self):
        r = Graph(self.nodes, self.edges)
        return r