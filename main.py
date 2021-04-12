from datetime import time
import csv
from typing import List, Any, Callable


class Node:

    def __init__(self, associated_value: Any = None):
        self.childs: List[Node] = []
        self.associated_value: Any = associated_value

    def add_child(self, child):
        self.childs.append(child)

    # TODO: поменять реализацию хэша на более удачную
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)


def deep_search(start_node: Node, func: Callable):
    """
    func must take 1 argument with type Node and return True when it`s searchble Node
    Return None when all nodes in graph were visited
    """
    visited = set()

    def deep_search_recursion(nodes: List[Node]):
        if len(nodes) == 0:
            return False, None

        nodes_for_next_step = []
        for node in nodes:
            if node not in visited:
                visited.add(node)

                is_searchble = func(node)
                if is_searchble:
                    return True, [node]
                else:
                    nodes_for_next_step += node.childs

        is_found, path = deep_search_recursion(nodes_for_next_step)
        if is_found:
            # TODO: придумать что-то более оптипальное
            head = None
            for node in nodes:
                if path[0] in node.childs:
                    head = node

            assert head is not None, "head mustn`t be None, logic error"
            return True, [head]+path

        return False, None

    is_found, path = deep_search_recursion([start_node])
    return path if is_found else None

# Это можно не читать, я и сам с трудом это читаю


def load_data():
    # TODO: сделать нормальную обработку данных
    with open('timetable.csv') as f:
        # csv.reader(f)
        place_time = {}
        for row in csv.DictReader(f, delimiter=';'):
            for key in row:
                if row[key].strip() != '':
                    place_time.setdefault(
                        tuple(key.split('->')), []).append(row[key])
        timetable = {
            key: tuple(
                tuple(map(time.fromisoformat, time_str.split('-')))
                for time_str in times
            )
            for key, times in place_time.items()
        }
        cities = {elem for pair in timetable for elem in pair}

        times = {
            v
            for e in timetable.values()
            for p in e
            for v in p
        }

    node_table = {
        city: {
            time: Node(city)
            for time in times
        }
        for city in cities
    }

    for city in node_table:
        time_stamps = sorted(node_table[city].keys())
        for first_time_stamp, last_time_stamp in zip(time_stamps[:-1], time_stamps[1:]):
            first_node = node_table[city][first_time_stamp]
            last_node = node_table[city][last_time_stamp]
            first_node.add_child(last_node)

    # for k,_ in timetable.keys():
    #     print(k,ord(k))
        
    # for k in node_table.keys():
    #     print(k,ord(k)) 
    # print(timetable.keys())
    # # print(node_table['A'])
    # # print(timetable['A'])
    # print(timetable)
    for from_city, to_sity in timetable:
        for first_time, last_time in timetable[(from_city,to_sity)]:
            node1 = node_table[from_city][first_time]
            node2 = node_table[to_sity][last_time]
            node1.add_child(node2)

            node1.associated_value += '-' + \
                first_time.isoformat(timespec='minutes')
            node2.associated_value += '-' + \
                last_time.isoformat(timespec='minutes')

    # TODO: выбор города
    return node_table['A'][min(node_table['A'].keys())]


graph = load_data()

path = deep_search(graph, lambda node: 'E' in node.associated_value)
if path:
    for node in path:
        print(node.associated_value, end=', ')
    print()
else:
    print(None)


# TESTS
# n1 = Node(1)
# n2 = Node(2)
# n3 = Node(3)
# n4 = Node(4)
# n5 = Node(5)
# n6 = Node(6)
# n7 = Node(7)

# n1.add_child(n2)
# n1.add_child(n3)

# n2.add_child(n3)
# n2.add_child(n4)

# n3.add_child(n5)

# n4.add_child(n6)

# n5.add_child(n7)

# n6.add_child(n7)

# path = deep_search(n1, lambda node: node.associated_value == 7)
# if path:
#     for node in path:
#         print(node.associated_value, end=', ')
#     print()
# else:
#     print(None)
