#!/usr/bin/env python3.5
import sys
import aoctools
import numpy as np
from collections import defaultdict
import math

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def calc_dist(x,y):
    return abs(x[0]-y[0])+abs(x[1]-y[1])

def get_base(asteroid_map,ith_asteroid):
    dim_x = len(asteroid_map[0])
    dim_y = len(asteroid_map)

    # make list of asteroid locations
    asteroid_locations = []
    for x in range(0,dim_x):
        for y in range(0,dim_y):
            if asteroid_map[y][x] == "#":
                asteroid_locations.append((x,y))

    # check best position
    max_asteroids = 0
    for location in asteroid_locations:
        asteroid_angles = defaultdict(int)
        for other_astroid in asteroid_locations:
            if location != other_astroid:
                up = (location[0],location[1]-1)
                angle = getAngle(up, location, other_astroid)
                asteroid_angles[int(angle*100)] += 1
        if len(asteroid_angles) > max_asteroids:
            max_pos = location[:]
            max_asteroids = len(asteroid_angles)


    # make list of pos from best asteroid_map
    asteroid_angles = defaultdict(list)
    for other_astroid in asteroid_locations:
        if location != other_astroid:
            up = (max_pos[0],max_pos[1]-1)
            angle = getAngle(up, max_pos, other_astroid)
            dist = calc_dist(max_pos,other_astroid)
            asteroid_angles[int(angle*1000)].append([other_astroid,dist])

    asteroid_angles = sorted(asteroid_angles.items(), key=lambda item: item[0])
    asteroid_angles_new=[]
    for angle in asteroid_angles:
        asteroid_angles_new.append((angle[0],sorted(angle[1], key=lambda item: item[1])))

    i = 0
    count = 0
    ith_asteroid_pos = []
    while len(asteroid_angles_new) > 1:
        count += 1
        if len(asteroid_angles_new[i][1]) == 1:
            ith_asteroid_pos = asteroid_angles_new.pop(i)[1]
        else:
            ith_asteroid_pos = asteroid_angles_new[i][1].pop(0)
            i = (i+1)%len(asteroid_angles_new)
        if count == ith_asteroid:
            break

    return [max_pos,max_asteroids,ith_asteroid_pos]




def run_tests():
    input_1= [".#..#",".....","#####","....#","...##"]
    #assert get_base(input_1,5) == [(3,4),8]
    input_2= ["......#.#.","#..#.#....","..#######.",".#.#.###..",".#..#.....","..#....#.#","#..#....#.",".##.#..###","##...#..#.",".#....####"]
    #assert get_base(input_2) == [(5,8),33]

    input = [".#..##.###...#######","##.############..##.",".#.######.########.#",".###.#######.####.#.","#####.##.#.##.###.##","..#####..#.#########","####################","#.####....###.#.#.##","##.#################","#####.##.###..####..","..######..##.#######","####.##.####...##..#",".#####..#.######.###","##...#.##########...","#.##########.#######",".####.#.###.###.#.##","....##.##.###..#####",".#.#.###########.###","#.#.#.#####.####.###","###.##.####.##.#..##"]
    #input = [".#....#####...#..","##...##.#####..##","##...#...#.#####.","..#.....#...###..","..#.#.....#....##"]
    print(get_base(input,200))
    print ("Tests passed")

if __name__ == '__main__':
    #run_tests()

    #input = aoctools.get_input(8,2019)
    puzzle_input=[".#..#..##.#...###.#............#.",".....#..........##..#..#####.#..#","#....#...#..#.......#...........#",".#....#....#....#.#...#.#.#.#....","..#..#.....#.......###.#.#.##....","...#.##.###..#....#........#..#.#","..#.##..#.#.#...##..........#...#","..#..#.......................#..#","...#..#.#...##.#...#.#..#.#......","......#......#.....#.............",".###..#.#..#...#..#.#.......##..#",".#...#.................###......#","#.#.......#..####.#..##.###.....#",".#.#..#.#...##.#.#..#..##.#.#.#..","##...#....#...#....##....#.#....#","......#..#......#.#.....##..#.#..","##.###.....#.#.###.#..#..#..###..","#...........#.#..#..#..#....#....","..........#.#.#..#.###...#.....#.","...#.###........##..#..##........",".###.....#.#.###...##.........#..","#.#...##.....#.#.........#..#.###","..##..##........#........#......#","..####......#...#..........#.#...","......##...##.#........#...##.##.",".#..###...#.......#........#....#","...##...#..#...#..#..#.#.#...#...","....#......#.#............##.....","#......####...#.....#...#......#.","...#............#...#..#.#.#..#.#",".#...#....###.####....#.#........","#.#...##...#.##...#....#.#..##.#.",".#....#.###..#..##.#.##...#.#..##"]

    result = get_base(puzzle_input,200)

    print("Solution for Puzzle 1: %i" %result[1])
    print("Solution for Puzzle 2: %i" %(result[2][0][0][0]*100 + result[2][0][0][1]))
