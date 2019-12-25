#!/usr/bin/env python3.6
import sys
import datetime
import aoctools

# def run_tests():
#     assert run_program(

def get_orbit(orbits,key):
    ret = 0
    if orbits[key] != 'COM':
        ret = 1

    return ret,orbits[key]

def calc_orbits(orbits):
    count = 0
    for obj in orbits.keys():
        next_obj = obj
        count += 1
        num = 'start'
        while num != 0:
            num, next_obj = get_orbit(orbits,next_obj)
            count += num

    return count

def calc_transition(orbits,key1,key2):
    key1_hist=[]
    key2_hist=[]
    while 1:
        if key1 != 'COM':
            _,key1 = get_orbit(orbits,key1)
            key1_hist.append(key1)
        if key2 != 'COM':
            _,key2 = get_orbit(orbits,key2)
            key2_hist.append(key2)
        if key2 in key1_hist:
            return key1_hist.index(key2) + len(key2_hist) -1
        if key1 in key2_hist:
            return key2_hist.index(key1) + len(key1_hist) -1

def run_tests():
    orbit_map_test1 = {'B':'COM', 'C':'B', 'D':'C', 'E':'D', 'F':'E', 'G':'B', 'H':'G', 'I':'D', 'J':'E', 'K':'J', 'L':'K'}
    orbit_map_test2 = {'B':'COM', 'C':'B', 'D':'C', 'E':'D', 'F':'E', 'G':'B', 'H':'G', 'I':'D', 'J':'E', 'K':'J', 'L':'K', 'YOU':'K','SAN':'I'}
    assert calc_orbits(orbit_map_test1) == 42
    assert calc_transition(orbit_map_test2,'YOU','SAN') == 4

if __name__ == '__main__':
    run_tests()
    print ("Tests passed")

    orbit_map = {x.split(")")[1]:x.split(")")[0] for x in aoctools.get_input(6,2019)}

    print("Solution for Puzzle 1: %i" %calc_orbits(orbit_map))
    print("Solution for Puzzle 2: %i" %calc_transition(orbit_map,'YOU','SAN'))
    start = datetime.datetime.now()
