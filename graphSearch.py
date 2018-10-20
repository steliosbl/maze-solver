from abc import ABC, abstractmethod
class GraphSearch(ABC):
    def __init__(self):
        pass
    
    def useGraph(self, graph):
        self.graph = graph

    @abstractmethod
    def search(self, entrance, exit):
        pass

    @abstractmethod
    def exportPath(self):
        pass
