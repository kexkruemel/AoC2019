#!/usr/bin/env python3.6
import sys
import aoctools
import numpy as np
from collections import defaultdict

def make_layers(input,w,h):
    input = [int(x) for x in input]
    input = np.array(input)
    print (input)
    i = 0
    no_zeros = np.Inf
    layers = []
    while w*h*i < len(input):
        layer = np.reshape(input[(w*h*i):(w*h*(i+1))],(h,w))
        layers.append(layer)
        unique, counts = np.unique(layer, return_counts=True)
        num_dict = defaultdict(int,zip(unique, counts))
        if num_dict[0] < no_zeros:
            ret = num_dict[1] * num_dict[2]
            no_zeros = num_dict[0]
        i += 1

    image = np.chararray((h,w))
    for y in range(h):
        for x in range(w):
            for layer in layers:
                if layer[y][x] == 0:
                    image[y][x] = '@'
                    break
                elif layer[y][x] == 1:
                    image[y][x] = '.'
                    break
    print (image)
    return ret



def run_tests():
    assert make_layers('123456789012',3,2)== 1

if __name__ == '__main__':
    run_tests()
    print ("Tests passed")

    input = aoctools.get_input(8,2019)

    print("Solution for Puzzle 1: %i" %make_layers(input[0],25,6))
    #print("Solution for Puzzle 2: %i" %calc_transition(orbit_map,'YOU','SAN'))
