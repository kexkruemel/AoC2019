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

def print_map(data):
    for line in data:
        printstring = ""
        for char in line:
            printstring += char
        print (printstring)

def lowercase():
    return range(97,123)

def uppercase():
    return range(65,91)

def get_uppercase(char):
    return chr(ord(char)-32)

def get_lowercase(char):
    return chr(ord(char)+32)

def make_graph(data):
    G = nx.Graph()
    for y in range(len(data)-1):
        for x in range(len(data[0])):
            if data[y][x] == "." or ord(data[y][x]) in uppercase():
                for (x2,y2) in neighbours((x,y)):
                    if 0 < x2 < len(data[0]) and 0 < y2 < len(data)-1 and data[y2][x2] == "." and data[y][x] == ".":
                        G.add_edge((x,y),(x2,y2), weight=1)
                    elif 0 < x2 < len(data[0]) and 0 < y2 < len(data)-1 and ord(data[y2][x2]) in uppercase() and data[y][x] != "#":
                        G.add_edge((x,y),(x2,y2), weight=weight_door)
                    elif 0 < x2 < len(data[0]) and 0 < y2 < len(data)-1 and ord(data[y][x]) in uppercase() and data[y2][x2] != "#":
                        G.add_edge((x,y),(x2,y2), weight=weight_door)

    return G

def find_key_door():
    min_dist = np.Inf
    min_key = ""
    # finding closest way of pos -> key -> door
    for key in nyckel:
        dist = nx.shortest_path_length(G, tuple(pos), nyckel[key],weight="weight")
        try:
            dist_door = nx.shortest_path_length(G, nyckel[key], doors[get_uppercase(key)],weight="weight")
        except:
            dist_door = 2*weight_door

        if dist+dist_door < weight_door*2:
            if dist+dist_door < min_dist:
                min_dist = dist+dist_door
                min_key = key
                print ("Overall path to get to door %c: %i" %(get_uppercase(key),dist+dist_door-weight_door))
    return min_key,min_dist-weight_door

def find_accessible_keys_with_doors():
    # finding closest way of pos -> key -> door
    accessible_keys=[]
    for key in nyckel_start:
        dist = nx.shortest_path_length(G, tuple(pos_start), nyckel_start[key],weight="weight")
        try:
            dist_door = nx.shortest_path_length(G, nyckel_start[key], doors_start[get_uppercase(key)],weight="weight")
        except:
            dist_door = 2*weight_door
        if dist+dist_door < weight_door*2:
            accessible_keys.append(key)
    return accessible_keys

def find_door():
    # finding closest way of pos -> door for existing keys
    min_dist = np.Inf
    min_door = ""
    dist_door = np.Inf
    for key in nyckel_pocket:
        door = get_uppercase(key)
        try:
            dist_door = nx.shortest_path_length(G, pos, doors[door],weight="weight")
        except:
            dist_door = 2*weight_door

        if dist_door < weight_door*2:
            if dist_door < min_dist:
                min_dist = dist_door
                min_door = door
                print ("Path to get to door %c: %i" %(door,dist_door-weight_door))
    return min_door,min_dist-weight_door

def go_to(goal):
    # go there and pocket all the keys on the way
    global count
    global nyckel
    global nyckel_pocket
    if verbose: print("Going from %s to %s"%(str(pos),str(goal)))
    path_len = nx.shortest_path_length(G, pos, goal)
    count += path_len
    path = nx.shortest_path(G, pos, goal)
    getkeys = []
    for waypoint in path:
        for key in nyckel:
            if nyckel[key] == waypoint: #check if there is a key to be picket up
                if verbose: print(colored("Getting key %c" %key,'green'))
                getkeys.append(key)
        for door in doors:
            if doors[door] == waypoint: #if there is a door check if you have a key, if yes reduce weight = open door
                if get_lowercase(door) in nyckel_pocket:
                    for (x,y) in neighbours(waypoint):
                        if 0 < x < len(data[0]) and 0 < y < len(data)-1 and data[y][x] == ".":
                            G.remove_edge(waypoint,(x,y))
                            G.add_edge(waypoint,(x,y), weight=1)
                else:
                    if verbose: print ("Don't have a key for door %c \n" %door)
                    return False

    for key in getkeys:
        # put keys in pocket and remove from map
        del nyckel[key]
        nyckel_pocket.append(key)

    return goal

def run_tests():
    assert iterate_phases("12345678",4) == "01029498"

    print ("Tests passed")

if __name__ == '__main__':
    #run_tests()
    start = datetime.datetime.now()
    verbose = False

    file_name = "018.txt"
    file = open(file_name, 'r').read()

    data = [list(line) for line in file.split("\n")]

    nyckel_start = defaultdict(list)
    doors_start = defaultdict(list)
    weight_door = 100000
    available_keys = []

    for y in range(len(data)-1):
        for x in range(len(data[0])):
            char = data[y][x]
            if char == "@":
                pos_start= (x,y)
                data[y][x] = "."
            elif ord(char) in lowercase():  # lowercase char
                nyckel_start[char] = (x,y)
                data[y][x] = "."
                available_keys.append(char)
            elif ord(char) in uppercase():  # uppercase char
                doors_start[char] = (x,y)

    print_map(data)
    G = make_graph(data)

    acessible_keys = find_accessible_keys_with_doors()
    print(acessible_keys)
    min_dist = np.Inf


    for key in acessible_keys:
        print ("Checking perms starting with %c"  %key)
        print("Took %s" %(datetime.datetime.now() -start))
        invalid_starts=defaultdict(list)
        for order in permutations([k for k in nyckel_start.keys() if k != key]):
            key_order = [key] + list(order)
            #print(key_order)
            pos = pos_start
            nyckel = nyckel_start.copy()
            doors = doors_start.copy()
            nyckel_pocket = []
            if verbose: print ("Checking order %s" %str(key_order))
            count = 0
            go_on = True
            for length in invalid_starts.keys():
                if key_order[:length] in invalid_starts[length]:
                    go_on = False
            if go_on:
                for k, dest_key in enumerate(key_order): #go through all keys
                    if dest_key not in nyckel_pocket: #if it's already collected, no need to go further
                        if verbose: print ("Going to key %c" %dest_key)
                        pos = go_to(nyckel[dest_key])
                        if pos == False: #will return false if there is a door in between
                            if verbose: print("Start %s is invalid" %str(key_order[:k+1]))
                            invalid_starts[k+1].append(key_order[:k+1])
                            if verbose: print("Invalid starts: %s" %str(invalid_starts))
                            break
                        if verbose: print("Keys in pocket: %s"%str(nyckel_pocket))
                        if verbose: print("Keys in map: %s" %str(nyckel))
                        if verbose: print("Current distance: %i" %count)
                    if count > min_dist:
                        if verbose: print("Already too big. Break")
                        break
            if verbose: print(count)
            if len(nyckel) == 0:
                if count < min_dist:
                    min_dist = count
                    print("Current Min: %i" %min_dist)

    print(min_dist)
    delta =  datetime.datetime.now() -start
    print("Took %s" %delta)
