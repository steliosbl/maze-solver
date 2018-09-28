from directions import directionToNumber

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
    