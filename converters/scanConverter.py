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
                                node.adjacents[0] = leftBuffer
                                leftBuffer.adjacents[2] = node
                                leftBuffer = node
                                self.edges.add(Edge(leftBuffer.position, node.position, x-leftBuffer.position[0] +1))
                                if below:
                                    upBuffer[x] = node
                                else:
                                    node.adjacents[1] = upBuffer[x]
                                    upBuffer[x].adjacents[3] = node
                                    self.edges.add(Edge(upBuffer[x].position, node.position, y-upBuffer[x].position[1] + 1))
                        
                        else: #WWB
                            node = Node((x,y))
                            self.nodes.add(node)
                            node.adjacents[0] = leftBuffer
                            leftBuffer.adjacents[2] = node
                            self.edges.add(Edge(leftBuffer.position, node.position, x-leftBuffer.position[0] +1))
                            if above:
                                node.adjacents[1] = upBuffer[x]
                                upBuffer[x].adjacents[3] = node
                                self.edges.add(Edge(upBuffer[x].position, node.position, y-upBuffer[x].position[1] + 1))
                            if below:
                                upBuffer[x] = node
                else:
                    if next: #BWW
                        node = Node((x,y))
                        self.nodes.add(node)
                        leftBuffer = node
                        if above:
                            node.adjacents[1] = upBuffer[x]
                            upBuffer[x].adjacents[3] = node
                            self.edges.add(Edge(upBuffer[x].position, node.position, y-upBuffer[x].position[1] + 1))
                        if below:
                            upBuffer[x] = node

                    else: #BWB
                        if above != below: #XOR
                            node = Node((x,y))
                            self.nodes.add(node)
                            if below:
                                upBuffer[x] = node
                            else:
                                node.adjacents[1] = upBuffer[x]
                                upBuffer[x].adjacents[3] = node
                                self.edges.add(Edge(upBuffer[x].position, node.position, y-upBuffer[x].position[1] + 1))


        exit = Node(self.whiteMap.endpoints[1])
        exit.adjacents[1] = upBuffer[exit.position[0]]
        self.nodes.add(exit)
        self.edges.add(Edge((exit.position[0], exit.position[1]-1), exit.position, 1))

    def exportGraph(self):
        r = Graph(self.nodes, self.edges)
        return r