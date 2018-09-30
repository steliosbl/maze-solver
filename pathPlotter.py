class PathPlotter:
    def __init__(self, img):
        self.img = img

    def plot(self, path):
        self.img = self.img.convert("RGB")
        pixels = self.img.load()
        for node in path:
            pixels[node] = (0,0,255)

    def save(self, filename):
        self.img.save(filename)
        
