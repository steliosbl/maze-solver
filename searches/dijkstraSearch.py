from graphSearch import GraphSearch
from heapq import heappush, heappop
from collections import defaultdict
import math

def keyed_bisect(lst, value, key=None):
    if key is None:
        key = lambda x: x
    def bis(lo, hi=len(lst)):
        while lo < hi:
            mid = (lo + hi) // 2
            if key(lst[mid]) < value:
                lo = mid + 1
            else:
                hi = mid
        return lo
    return bis(0)

class DijkstraSearch(GraphSearch):
    def __init__(self):
        self.queue = [] 
        self.prev = {}
    
    def search(self, entrance, exit):
        self.entrance = entrance
        self.exit = exit

        entrance.working = 0
        self.queue.append(entrance)
        while self.queue:
            current = self.queue.pop(0)
            current.finalized = True
            for i in range(4):
                node = current.adjacents[i]
                if node and not node.finalized:
                    total_dist = current.working + current.distances[i]
                    if not node.working or total_dist < node.working:
                        if node.working:
                            self.queue.remove(node)
                        node.working = total_dist
                        self.prev[node] = current
                        self.queue.insert(keyed_bisect(self.queue, total_dist, lambda node:node.working), node)
        
    def exportPath(self):
        result = []
        current = self.exit
        while current != self.entrance:
            result.append(current)
            current = self.prev[current]
        result.append(self.entrance)
        return result




