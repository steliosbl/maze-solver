from PIL import Image
import whiteMap
from timeit import default_timer as timer
from mapToGraphConverter import MapToGraphConverter
from graphToImageConverter import GraphToImageConverter


og = Image.open("mazes/perfect2k.png")

wm = whiteMap.WhiteMap.fromImage(og)
i= wm.toImage()
i.save("i.png")

converter = MapToGraphConverter(wm)
converter.convert()
g = converter.export()

a = GraphToImageConverter(g, wm)
i = a.convert()

i.save('b.png')
print("t")

# graph = Graph.fromWhiteMap(wm)

# print(search.dijkstra(graph, wm.entrance, wm.exit))