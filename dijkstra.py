graph = {
    0: {1: [6], 2: [2]},
    1: {3: [1]},
    2: {1: [3], 3: [5]},
    3: {}
}



def make_matrix(graph):
    matrix = [0] * len(graph)
    for i in graph.keys():
        matrix[i] = [float("inf")] * len(graph)
    for i in graph.keys():
        for j in graph[i].keys():
            matrix[i][j] = graph[i][j][0]
    return matrix

def dijkstra(graph, start_node, end_node):
    matrix = make_matrix(graph)
    amount_nodes = len(matrix)
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
            print(costs[k])
            if costs[min_cost_index] + matrix[min_cost_index][k] < costs[k]:
                costs[k] = costs[min_cost_index] + matrix[min_cost_index][k]
        not_visited[min_cost_index] = False
    return costs[end_node]

print("Наименьшее время:", dijkstra(graph, 0, 3), "минут")

