#!/usr/bin/env python3.5
import sys
import aoctools
import numpy as np
from collections import defaultdict
from itertools import combinations, count
from functools import reduce
from math import gcd


def calc_motion(moon_pos,steps):
    moon_vel = np.zeros((4,3))
    moon_pos_orig = moon_pos[:]

    for j in range(1,steps+1):
        pairs = combinations(range(4), 2)
        for moon1,moon2 in pairs:
            for axis in range(3):
                if moon_pos[moon1][axis] > moon_pos[moon2][axis]:
                    moon_vel[moon1][axis] -= 1
                    moon_vel[moon2][axis] += 1
                elif moon_pos[moon1][axis] < moon_pos[moon2][axis]:
                    moon_vel[moon1][axis] += 1
                    moon_vel[moon2][axis] -= 1

        moon_pos = moon_pos + moon_vel


        for_hist = list(np.append(moon_pos[axis],moon_vel[axis]))
        if for_hist == moon_pos_orig[axis]:
            print("%i cycles to origin after %i steps" %(axis,j))

        if j%10000 == 0:
            print(j)

    kin = np.sum(abs(moon_vel),axis = 1)
    pot = np.sum(abs(moon_pos),axis = 1)
    return (sum(kin*pot))

def _system_axis_state(moons, axis):
    # return (
    #     *(moons[m][0][axis] for m in range(4)),
    #     *(moons[m][1][axis] for m in range(4)),
    # )
    return (
        moons[0][0][axis],
        moons[1][0][axis],
        moons[2][0][axis],
        moons[3][0][axis],
        moons[0][1][axis],
        moons[1][1][axis],
        moons[2][1][axis],
        moons[3][1][axis],
    )

def calc_rep(moon_pos,axis):
    moons = [[list(pos), [0, 0, 0]] for pos in moon_pos]
    start_state = _system_axis_state(moons, axis)

    moon_pairs = list(combinations(moons, 2))

    first_loop = True
    for steps in count():
        if _system_axis_state(moons, axis) == start_state and not first_loop:
            return steps
        first_loop = False

        for (position_a, velocity_a), (position_b, velocity_b) in moon_pairs:
            if position_a[axis] < position_b[axis]:
                velocity_a[axis] += 1
                velocity_b[axis] -= 1
            elif position_a[axis] > position_b[axis]:
                velocity_a[axis] -= 1
                velocity_b[axis] += 1

        for pos, v in moons:
            pos[axis] += v[axis]

def  calc_rep_all(moon_pos):
    return lcm((calc_rep(moon_pos, axis) for axis in range(3)))

def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)

def run_tests():
    assert calc_motion(np.array([[-1,0,2],[2,-10,-7],[4,-8,8],[3,5,-1]]),10) == 179
    assert calc_motion(np.array([[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]]),100) == 1940
    assert calc_rep_all(np.array([[-1,0,2],[2,-10,-7],[4,-8,8],[3,5,-1]])) == 2772
    assert calc_rep_all(np.array([[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]])) == 4686774924

if __name__ == '__main__':
    run_tests()
    print ("Tests passed")

    input = aoctools.get_input(12,2019)

    print("Solution for Puzzle 1: %i" %calc_motion(np.array([[-4,3,15],[-11,-10,13],[2,2,18],[7,-1,0]]),1000))
    print("Solution for Puzzle 2: %i" %calc_rep_all(np.array([[-4,3,15],[-11,-10,13],[2,2,18],[7,-1,0]])))
