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
args = parser.parse_args()

print("Loading image to memory..")
og = Image.open(args.maze)
wm = WhiteMap.fromImage(og)

print("Converting to graph..")
conversion_start = timer()
converter = converters[args.converter]()
converter.useWhiteMap(wm)
converter.convert()
graph = converter.exportGraph()
conversion_end = timer()
print("Conversion took {0} seconds".format(str(conversion_end-conversion_start)))

print("Searching graph..")
search_start = timer()
search = searches[args.search]()
search.useGraph(graph)
search.find()
path = search.exportPath()
search_end = timer()
print("Search took {0} seconds".format(str(search_end-search_start)))

print("Drawing path..")
plotter = PathPlotter(og)
plotter.plot(path)
plotter.save(args.outname)
print("Solved maze saved as {0}".format(args.outname))
