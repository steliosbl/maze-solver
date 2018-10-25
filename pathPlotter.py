class PathPlotter:
    def __init__(self, img):
        self.img = img

    def plot(self, path):
        self.img = self.img.convert("RGB")
        pixels = self.img.load()
        for i in range(1, len(path)):
            current = path[i-1]
            next = path[i]
            if current.position[0] == next.position[0]:
                coefficient = 1
                if next.position[1] - current.position[1] < 0:
                    coefficient = -1
                positions = [(current.position[0], i) for i in range(current.position[1], next.position[1], coefficient)]
            else:
                coefficient = 1
                if next.position[0] - current.position[0] < 0:
                    coefficient = -1
                positions = [(i, current.position[1]) for i in range(current.position[0], next.position[0], coefficient)]
            positions += [current.position,next.position]
            for p in positions:
                pixels[p] = (0,0,255)
            #pixels[node.position] = (0,0,255)

    def save(self, filename):
        self.img.save(filename)
        
