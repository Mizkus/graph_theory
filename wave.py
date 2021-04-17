
from collections import deque
from typing import Dict, List

import data


def wave(graph: Dict[str, List[str]], start_node: str):
    if start_node not in graph:
        raise RuntimeError(
            "Данного города нет или в указанное время из него не отправляются автобусы")

    path_table = {node: None for node in graph}
    queue = deque([start_node])
    visited = set()

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for child in graph[node]:
                path_table[child] = path_table[child] or node
                queue.append(child)
    return path_table


def convert_to_out_format(nodes: List[str]):
    from_to = []
    start_city = convert_to_out_format_node_name(nodes[0])
    for i, elem in enumerate(nodes[1:], start=1):
        cur_city = convert_to_out_format_node_name(elem)
        if cur_city != start_city:
            from_to.append((nodes[i-1], nodes[i]))
            start_city = cur_city
    return tuple(from_to)

def convert_to_out_format_node_name(node):
    node_name = ""
    for i in node:
        if i.isalpha():
            node_name += i
    return node_name

def my_super_algorithm(graph: Dict[str, List[str]], start_node: str, required: str):
    path_table = wave(graph, start_node)
    for node in sorted(filter(lambda x: required in x, graph)):
        if path_table[node] is not None:
            cur = node
            path = []
            while cur:
                path.append(cur)
                cur = path_table[cur]
            return convert_to_out_format(path[::-1])

    else:
        raise RuntimeError(
            "Попытайся доехать до нужного места завтра, сегодня тебе не удастся")

if __name__ == "__main__":
    graph = data.load_data()
    # TODO: закоментировать если нужно сделать выбор
    city = input("Введите название города: ")
    time = input("Введите время отправки (Например 13:45): ")
    required = input("Введите конечный пункт: ")

    # TODO: раскоментировать если выбирается конкретный город
    # city = 'A'
    # time = '10:00'
    # required = 'E'

    try:
        way = my_super_algorithm(graph, city+time, required)
        for from_to in way: 
            print(*from_to,sep='->')
    except Exception as e:
        print(e)
