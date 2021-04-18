def index_convert_graph(graph, start_node = None, end_node = None):
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
    graph_index = dict()
    for i in range(len(graph)):
        graph_index[i] = {}
    for i in graph.keys():
        for j, l in graph[i].items():
            temp1 = index_convert_graph(graph)[0][i]
            temp2 = index_convert_graph(graph)[0][j]
            graph_index[temp1][temp2] = l
    return graph_index

def make_matrix(graph):
    graph = graph_converter(graph)
    matrix = [0] * len(graph)
    for i in graph.keys():
        matrix[i] = [float("inf")] * len(graph)
    for i in range(len(graph)):
        for j in graph[i].keys():
            matrix[i][j] = graph[i][j][0]
    return matrix

def dijkstra(graph, start_node, end_node):
    start_node = index_convert_graph(graph, start_node)[1]
    end_node = index_convert_graph(graph, end_node=end_node)[2]
    matrix = make_matrix(graph)
    amount_nodes = len(matrix)
    parents = [None] * amount_nodes
    not_visited = [True]*amount_nodes
    costs = [float("inf")]*amount_nodes
    costs[start_node] = 0
    for i in range(amount_nodes):
        min_cost = float("inf")
        min_cost_index = -1
        for j in range(amount_nodes):
            if not_visited[j] and costs[j] < min_cost:
                min_cost = costs[j]
                min_cost_index = j 
        for k in range(amount_nodes):
            if costs[min_cost_index] + matrix[min_cost_index][k] < costs[k]:
                costs[k] = costs[min_cost_index] + matrix[min_cost_index][k]
                parents[k] = index_convert_graph(graph)[3][min_cost_index]
        not_visited[min_cost_index] = False
    path = [index_convert_graph(graph)[3][end_node]]
    parent = parents[end_node]
    while not parent is None:
        path.append(parent)
        parent = parents[index_convert_graph(graph)[0][parent]]
    return (costs[end_node], path[::-1])

if __name__ == "__main__":

    graph = {
        "A": {"C": [6], "D": [2]},
        "C": {"B": [1]},
        "D": {"C": [3], "B": [5]},
        "B": {}
    }

    # TODO: раскоментировать если нужно сделать выбор
    #start_node, end_node = map(str, input("Введите начальный и конечный узел, через пробел: ").split())

    #TODO: закоментировать если нужно сделать выбор
    start_node = "A"
    end_node = "B"

    dijkstra_output = dijkstra(graph, start_node, end_node)
    print("Минимальное время: ", dijkstra_output[0], "минут")
    print(*dijkstra_output[1], sep = "->")




