
from collections import deque, defaultdict
from typing import Dict, List
from functools import lru_cache
import data


def wave(graph: Dict[str, List[str]], start_node: str):
    if start_node not in graph:
        raise RuntimeError(
            "Данного города нет или в указанное время из него не отправляются автобусы")

    path_table = defaultdict(set)
    queue = deque([start_node])
    visited = set()

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for child in graph[node]:
                # Если path_table[child]==None, тогда значение изменится, иначе останется прежним
                path_table[child].add(node)
                queue.append(child)
    # for k in path_table:
    #     print(k,':',path_table[k])
    # print(path_table)
    return path_table


def convert_to_out_format(nodes: List[str]):
    from_to = []
    # переделать для названия города произвольной длины, а не только единичной
    start_city = nodes[0][0]
    for i, elem in enumerate(nodes[1:], start=1):
        cur_city = elem[0]  # переделать!!!
        if cur_city != start_city:
            from_to.append((nodes[i-1], nodes[i]))
            start_city = cur_city
    return tuple(from_to)


def my_super_algorithm(graph: Dict[str, List[str]], start_node: str, required_city: str):
    path_table = wave(graph, start_node)

    @lru_cache
    def get_ways(cur):
        if path_table[cur] == {}:
            return []
        ways = []
        for node in path_table[cur]:
            if required_city not in node:
                way_parts = get_ways(node)
                if way_parts == []:
                    ways.append([node])
                for path in get_ways(node):
                    ways.append([cur]+path)
        return ways

    ways = []
    for node in sorted(filter(lambda x: required_city in x, graph)):
        if path_table[node] != {}:
            for path in get_ways(node):
                formated_path = convert_to_out_format(path[::-1])
                ways.append(formated_path)

    if ways == []:
        raise RuntimeError(
            "Попытайся доехать до нужного места завтра, сегодня тебе не удастся")
    return sorted(set(ways))


if __name__ == "__main__":
    graph = data.load_model()
    # TODO: раскоментировать если нужно сделать выбор
    # city = input("Введите название города: ")
    # time = input("Введите время отправки (Например 13:45): ")
    # required = input("Введите конечный пункт)

    # TODO: закоментировать если выбирается конкретный город
    city = 'A'
    time = '10:00'
    required = 'E'

    try:
        ways = my_super_algorithm(graph, city+time, required)
        for path in ways:
            print(path)
    except Exception as e:
        print(e)
