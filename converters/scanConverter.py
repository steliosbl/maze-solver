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
        upBuffer = [None] * self.whiteMap.x
        upBuffer[self.whiteMap.endpoints[0][0]] = Node(self.whiteMap.endpoints[0])
        self.nodes.add(Node(self.whiteMap.endpoints[0]))
        for y in range(self.whiteMap.y-1): #Do not check last row
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
                                leftBuffer = node
                                self.edges.add(Edge(leftBuffer.position, node.position, cost))
                                if below:
                                    upBuffer[x] = node
                                else:
                                    cost = y-upBuffer[x].position[1] + 1
                                    node.adjacents[1] = upBuffer[x]
                                    node.distances[1] = cost
                                    upBuffer[x].adjacents[3] = node
                                    upBuffer[x].distances[3] = cost
                                    self.edges.add(Edge(upBuffer[x].position, node.position, cost))
                        
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
                                if below:
                                    upBuffer[x] = node
                                else:
                                    cost = y-upBuffer[x].position[1] + 1
                                    node.adjacents[1] = upBuffer[x]
                                    node.distances[1] = cost
                                    upBuffer[x].adjacents[3] = node
                                    upBuffer[x].distances[3] = cost
                                    self.edges.add(Edge(upBuffer[x].position, node.position, cost))


        exit = Node(self.whiteMap.endpoints[1])
        exit.adjacents[1] = upBuffer[exit.position[0]]
        exit.distances[1] = 1
        self.nodes.add(exit)
        self.edges.add(Edge((exit.position[0], exit.position[1]-1), exit.position, 1))

    def exportGraph(self):
        r = Graph(self.nodes, self.edges)
        return r