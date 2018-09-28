from PIL import Image
from enum import Enum

class Color(Enum):
    Node = (255,0,0)
    Edge = (0,0,255)
    Path = (0,255,0)
    Wall = (0,0,0)

class GraphToImageConverter:
    def __init__(self, graph, whiteMap):
        self.graph = graph
        self.whiteMap = whiteMap
    
    def convert(self):
        img = Image.new("RGB", (self.whiteMap.x, self.whiteMap.y),0)
        pixels = img.load()
        for edge in self.graph.edges:
            pixels[edge.start] = Color.Node.value
            pixels[edge.end] = Color.Node.value
            if edge.start[1] == edge.end[1]:
                start = edge.start[0]
                end = edge.end[0]
                if start > end:
                    start,end = end,start
                for i in range(start+1, end):
                    pixels[i, edge.start[1]] = Color.Edge.value
            else:
                start = edge.start[1]
                end = edge.end[1]
                if start > end:
                    start,end = end,start
                for i in range(start+1, end):
                    pixels[edge.start[0], i] = Color.Edge.value
        for y in range(self.whiteMap.y):
            for x in range(self.whiteMap.x):
                if self.whiteMap[x,y]:
                    if  pixels[x,y] == (0,0,0):
                        pixels[x,y] = (255,255,255)
        return img