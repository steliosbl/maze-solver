from PIL import Image
from whiteMap import WhiteMap
from timeit import default_timer as timer
from converters import all as converters
from searches import all as searches
import argparse
from pathPlotter import PathPlotter

parser = argparse.ArgumentParser(description="Solve (theoretically) any maze!")
parser.add_argument("maze", type=argparse.FileType("rb"), help="The maze to be solved. Must be in image form.")
parser.add_argument("-c","--converter", dest="converter", choices=converters.keys(), default="scan", help="The algorithm that will be used to convert the maze from image to graph form.")
parser.add_argument("-s", "--search", dest="search", choices=searches.keys(), default="dijkstra", help="The algorithm that will be used to find the optimal path to the exit.")
parser.add_argument("-o", "--output", dest="outname", default="solved.png", help="The path of the file the solution will be outputted to")
parser.add_argument("-g", "--graph", dest="graph_mode", action="store_true", help="DEBUG FEATURE: Do not attempt to solve, simply project the graph on to the maze image. Used to debug converters.")
args = parser.parse_args()

print("Loading image to memory..")
og = Image.open(args.maze)
wm = WhiteMap.fromImage(og)

print("Locating endpoints..")
wm.getEndpoints()
if len(wm.endpoints) != 2:
    raise ValueError("Invalid number of endpoints")


print("Converting to graph..")
conversion_start = timer()
converter = converters[args.converter]()
converter.useWhiteMap(wm)
converter.convert()
graph = converter.exportGraph()
graph.getEndpoints(wm.endpoints)
conversion_end = timer()
print("Conversion took {0} seconds".format(str(conversion_end-conversion_start)))

if args.graph_mode:
    print("Drawing graph..")
    plotter = PathPlotter(og)
    plotter.displayGraph(graph)
    plotter.save(args.outname)
    print("Solved maze saved as {0}".format(args.outname))
else:
    print("Searching graph..")
    search_start = timer()
    search = searches[args.search]()
    search.useGraph(graph)
    search.search(graph.entrance, graph.exit)
    path = search.exportPath()
    search_end = timer()
    print("Search took {0} seconds".format(str(search_end-search_start)))

    print("Drawing path..")
    plotter = PathPlotter(og)
    plotter.plot(path)
    plotter.save(args.outname)
    print("Solved maze saved as {0}".format(args.outname))
