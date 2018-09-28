from collections import deque
infinity = float('inf')
def dijkstra(graph, source, dest):
    assert source in graph.vertices, 'Such source node doesn\'t exist'

    # 1. Mark all nodes unvisited and store them.
    # 2. Set the distance to zero for our initial node 
    # and to infinity for other nodes.
    distances = {vertex: infinity for vertex in graph.vertices}
    previous_vertices = {
        vertex: None for vertex in graph.vertices
    }
    distances[source] = 0
    vertices = graph.vertices.copy()

    while vertices:
        # 3. Select the unvisited node with the smallest distance, 
        # it's current node now.
        current_vertex = min(
            vertices, key=lambda vertex: distances[vertex])

        # 6. Stop, if the smallest distance 
        # among the unvisited nodes is infinity.
        if distances[current_vertex] == infinity:
            break

        # 4. Find unvisited neighbors for the current node 
        # and calculate their distances through the current node.
        for neighbour, cost in graph.neighbours[current_vertex]:
            alternative_route = distances[current_vertex] + cost

            # Compare the newly calculated distance to the assigned 
            # and save the smaller one.
            if alternative_route < distances[neighbour]:
                distances[neighbour] = alternative_route
                previous_vertices[neighbour] = current_vertex

        # 5. Mark the current node as visited 
        # and remove it from the unvisited set.
        vertices.remove(current_vertex)


    path, current_vertex = deque(), dest
    while previous_vertices[current_vertex] is not None:
        path.appendleft(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    if path:
        path.appendleft(current_vertex)
    return path