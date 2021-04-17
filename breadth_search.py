def breadth_search(graph, start_node, end_node):
    from collections import deque
    start_vertex = start_node
    end_vertex = end_node
    visited = [start_node]
    queue = deque([start_node])
    parents = [None] * len(graph)
    while queue:
        node = queue.popleft()
        for neighbour_node in graph[node]:
            if neighbour_node not in visited:
                visited.append(neighbour_node)
                parents[neighbour_node] = node
                queue.append(neighbour_node)
    path = [end_node]
    parent = parents[end_node]
    while not parent is None:
        path.append(parent)
        parent = parents[parent]
    return len(path[::-1]) - 1

graph = {
    0: [1, 2],
    1: [3],
    2: [4],
    3: [4],
    4: [5],
    5: []
}
print("Наименьшее необходимое количество шагов: ", breadth_search(graph, 0, 5))