class WhiteMap:
    def __init__(self, _):
        self._ = _
        self.y = len(_)
        self.x = len(_[0])
    
    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self._[key[1]][key[0]]
        else:
            return self._[key]

    def fromImage(img):
        pixels = img.load()
        wm = [[bool(pixels[i,j]) for i in range(img.size[0])] for j in range(img.size[1])]
        return WhiteMap(wm)

    def getAdjacents(self, x, y):
        #         r = [(-1,-1),(-1,-1),(-1,-1),(-1,-1)]
        # if x != 0:
        #     r[0]=(y, x-1)
        # if y != 0:
        #     r[1]=(y-1, x)
        # if x != self.x - 1:
        #     r[2]=(y, x+1)
        # if y != self.y - 1:
        #     r[3]=(y+1,x)
        # return r
        r = []
        if x != 0:
            r.append((y, x-1))
        if y != 0:
            r.append((y-1, x))
        if x != self.x - 1:
            r.append((y, x+1))
        if y != self.y - 1:
            r.append((y+1,x))
        return r

    def getWhiteAdjacents(self, adjacents):
        return [a for a in adjacents if self[a[0]][a[1]]]

    