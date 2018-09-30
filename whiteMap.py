from PIL import Image
from mapToGraphConverter import MapToGraphConverter

class WhiteMap:
    def __init__(self, _):
        self._ = _
        self.y = len(_)
        self.x = len(_[0])
        self.entrance = self.get_entrance()
        self.exit = self.get_exit()
    
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

    def fromImage(img):
        pixels = img.load()
        wm = [[bool(pixels[i,j]) for i in range(img.size[0])] for j in range(img.size[1])]
        return WhiteMap(wm)

    def fromDimensions(x,y):
        return WhiteMap([[False for i in range(x)] for j in range(y)])

    def toImage(self):
        img = Image.new("1", (self.x, self.y))
        pixels = img.load()
        for y in range(self.y):
            for x in range(self.x):
                pixels[x,y] = int(self[x,y])
        return img

    def toGraph(self, converter):
        if not isinstance(converter, MapToGraphConverter):
            raise TypeError("Provided converter is not instance of the required abstract class MapToGraphConverter")
        converter.useWhiteMap(self)
        converter.convert()
        return converter.exportGraph()

    def get_entrance(self):
        for x in range(self.x):
            if self[x,0]:
                return (x,0)

    def get_exit(self):
        for x in range(self.x):
            if self[x,self.y-1]:
                return (x,self.y-1)