def index_convert_graph(graph, start_node = None, end_node = None):
    # Присваивает индекс каждому узлу графа
    key_index = dict()
    value_index = dict()
    c = 0
    for k in graph.keys():
        key_index[k] = c
        value_index[c] = k
        c += 1
    if start_node != None: start_node = key_index[start_node]
    if end_node != None: end_node = key_index[end_node]
    return (key_index, start_node, end_node, value_index)

def graph_converter(graph):
    # Возвращает индексированный граф
    graph_index = dict()
    for i in range(len(graph)):
        graph_index[i] = {}
    for i in graph.keys():
        for j in graph[i]:
            temp1 = index_convert_graph(graph)[0][i]
            temp2 = index_convert_graph(graph)[0][j]
            graph_index[temp1] = [temp2]
    return graph_index

def breadth_search(graph, start_node, end_node):
    # Возвращает кортеж (колличество шагов, путь)
    from collections import deque
    graph_index = graph_converter(graph)
    start_node = index_convert_graph(graph, start_node)[1]
    end_node = index_convert_graph(graph, end_node = end_node)[2]
    visited = [start_node]
    queue = deque([start_node])
    parents = [None] * len(graph_index)
    while queue:
        node = queue.popleft()
        for neighbour_node in graph_index[node]:
            if neighbour_node not in visited:
                visited.append(neighbour_node)
                parents[neighbour_node] = index_convert_graph(graph)[3][node]
                queue.append(neighbour_node)
    path = [index_convert_graph(graph)[3][end_node]]
    parent = parents[end_node]
    while not parent is None:
        path.append(parent)
        parent = parents[index_convert_graph(graph)[0][parent]]
    return (len(path) - 1, path[::-1])

if __name__ == "__main__":

    graph = {
        "A": ["E", "C"],
        "C": ["D"],
        "D": ["B"],
        "E": ["F"],
        "F": ["D"],
        "B": []
    }
    # TODO: раскоментировать если нужно сделать выбор
    #start_node, end_node = map(str, input("Введите начальный и конечный узел, через пробел: ").split())

    #TODO: закоментировать если нужно сделать выбор
    start_node = "A"
    end_node = "B"

    breadth_search_output = breadth_search(graph, start_node, end_node)

    print("Наименьшее необходимое количество шагов: ", breadth_search_output[0])
    print(*breadth_search_output[1], sep = "->")