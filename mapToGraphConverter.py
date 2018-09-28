from abc import ABC, abstractmethod
class MapToGraphConverter(ABC):
    def __init__(self):
        pass
    
    def useWhiteMap(self, whiteMap):
        self.whiteMap = whiteMap

    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def exportGraph(self):
        pass