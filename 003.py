#!/usr/bin/env python3.5
import numpy as np
import aoctools



directions = {"D" : [+1,0],
              "U" : [-1,0],
              "R" : [0,+1],
              "L" : [0,-1]}

def draw_wire(wire):
    position = [0,0]
    len = 0
    line ={}
    for direction in wire:
        for _ in range(int(direction[1:])):
            len += 1
            position += np.array(directions[direction[0]])
            line[tuple(position[:])] = len

    return line

def calc_crossing(first_wire,second_wire):
    first_wire = first_wire.split(',')
    second_wire = second_wire.split(',')

    line1 = draw_wire(first_wire)
    line2 = draw_wire(second_wire)

    crossings = set(tuple(i) for i in line1.keys()) & set(tuple(i) for i in line2.keys())

    #calculate min manhattan distance
    min_manhattan = min(np.sum(abs(np.array(list(crossings))),axis=1))
    # calculate min distance to crossing via wires
    min_wires = min([line1[item] + line2[item] for item in crossings])

    return (min_manhattan,min_wires)

def run_tests():
    assert calc_crossing('R8,U5,L5,D3','U7,R6,D4,L4') == (6,30)
    assert calc_crossing('R75,D30,R83,U83,L12,D49,R71,U7,L72','U62,R66,U55,R34,D71,R55,D58,R83') == (159,610)
    assert calc_crossing('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51','U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == (135,410)

if __name__ == '__main__':
    run_tests()
    print ("Tests passed")

    [wire1,wire2] = aoctools.get_input(3,2019)
    
    solution = calc_crossing(wire1,wire2)
    print("Solution for Puzle 1: %i " %solution[0])
    print("Solution for Puzle 1: %i " %solution[1])
