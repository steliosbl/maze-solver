class PathPlotter:
    def __init__(self, img):
        self.img = img

    def get_intermediate_positions(self, start, end):
        if start[0] == end[0]:
            step = 1
            if end[1] - start[1] < 0:
                step = -1
            positions = [(start[0],i) for i in range(start[1], end[1], step)]
        else:
            step = 1
            if end[0] - start[0] < 0:
                step = -1
            positions = [(i, start[1]) for i in range(start[0], end[0], step)]
        return positions

    def plot(self, path):
        self.img = self.img.convert("RGB")
        pixels = self.img.load()
        for i in range(1, len(path)):
            start = path[i-1].position
            end = path[i].position
            positions = self.get_intermediate_positions(start, end) + [start,end]
            for p in positions:
                pixels[p] = (0,0,255)

    def displayGraph(self, graph):
        self.img = self.img.convert("RGB")
        pixels = self.img.load()
        for edge in graph.edges:
            for pos in self.get_intermediate_positions(edge.start, edge.end):
                pixels[pos] = (0,0,255)
        for node in graph.nodes:
            pixels[node.position] = (255,0,0)

    def save(self, filename):
        self.img.save(filename)
        
