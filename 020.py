#!/usr/bin/env python3.5
import aoctools
from collections import defaultdict
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
from itertools import permutations
import datetime

def neighbours(pos):
    x = pos[0]
    y = pos[1]
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def lowercase():
    return range(97,123)

def uppercase():
    return range(65,91)

def print_map(data):
    for line in data:
        printstring = ""
        for char in line:
            printstring += char
        print (printstring)


def make_graph(data):
    G = nx.Graph()
    portals = defaultdict(list)
    for y in range(len(data)):
        for x in range(len(data[2])):
            if ord(data[y][x]) in uppercase():
                for (x2,y2) in neighbours((x,y)):
                    if 0 < x2 < len(data[0]) and 0 < y2 < len(data) and ord(data[y2][x2]) in uppercase():
                        one = data[y][x]
                        two = data[y2][x2]
                        x_one,y_one = x,y
                        x_two,y_two = x2,y2
                        data[y][x] = " "
                        data[y2][x2] = " "
                for (x3,y3) in neighbours((x_one,y_one)): # either point is close to first letter
                    if 0 < x3 < len(data[0]) and 0 < y3 < len(data) and data[y3][x3] == ".":
                        if (one,two) == ('A','A'): start = (x3,y3)
                        elif (one,two) == ('Z','Z'): end = (x3,y3)
                        else: portals[(one,two)].append((x3,y3))
                for (x3,y3) in neighbours((x_two,y_two)): # or point is close to second letter
                    if 0 < x3 < len(data[0]) and 0 < y3 < len(data) and data[y3][x3] == ".":
                        if (one,two) == ('A','A'): start = (x3,y3)
                        elif (one,two) == ('Z','Z'): end = (x3,y3)
                        else: portals[(one,two)].append((x3,y3))
            if data[y][x] == ".":
                for (x2,y2) in neighbours((x,y)):
                    if 0 < x2 < len(data[0]) and 0 < y2 < len(data) and data[y2][x2] == ".":
                        G.add_edge((x,y),(x2,y2))
    print_map(data)
    print(portals)
    for portal in portals:
        G.add_edge(portals[portal][0],portals[portal][1])


    return G,start,end

if __name__ == '__main__':
    #run_tests()
    time_start = datetime.datetime.now()
    verbose = False

    file_name = "020.txt"
    file = open(file_name, 'r').read()

    data = [list(line) for line in file.split("\n")]

    print_map(data)
    G,start,end = make_graph(data)
    print(nx.shortest_path_length(G, start, end))

    delta =  datetime.datetime.now() -time_start

    print("Took %s" %delta)
