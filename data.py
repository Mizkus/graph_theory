import datetime
import csv
from collections import defaultdict
from typing import Dict, List


def make_net(timepoints, nodes):
    net = {
        node+timepoint.strftime('%H:%M'): []
        for timepoint in timepoints
        for node in nodes
    }
    timepoints = sorted(timepoints)
    for node in nodes:
        for tp1, tp2 in zip(timepoints[:-1], timepoints[1:]):
            key1 = node+tp1.strftime('%H:%M')
            key2 = node+tp2.strftime('%H:%M')
            net[key1].append(key2)
    return net


def connect_elements_in_net(net: Dict[str, List], timetable: Dict[str, List]): 
    for from_to_scheme,periods in timetable.items():
        from_city,to_city = from_to_scheme.split('->')
        for period in periods:
            start_time,end_time = period.split('-')
            net[from_city+start_time].append(to_city+end_time)

def load_data():
    timetable = defaultdict(list)
    intervals_in_string = set()
    with open('timetable.csv') as f:
        for row in csv.DictReader(f, delimiter=';'):
            for k, v in row.items():
                if v != '':
                    timetable[k].append(v)
                    intervals_in_string.add(v)
    timepoints = {
        point for interval in intervals_in_string
        for point in map(
            lambda arg: datetime.datetime.strptime(arg, '%H:%M'), interval.split('-'))
    }
    nodes = {
        city for cities in timetable
        for city in cities.split('->')
    }
    net = make_net(timepoints, nodes)
    connect_elements_in_net(net, timetable)
    return net

