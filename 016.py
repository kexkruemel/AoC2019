#!/usr/bin/env python3.5
import sys
import aoctools
import numpy as np

def calc_phase(nums):
    pattern=[0, 1, 0, -1]

    ret = ""
    length = len(nums)
    for phase in range(1,length+1):
        print(phase)
        if 3*phase-1 > length:
            mul_array = np.repeat(pattern[0:3], phase) # nur pattern 0:3 muss repeated werden
        elif 2*phase-1 > length:
            mul_array = np.repeat(pattern[0:2], phase)
        elif 1*phase-1 > length:
            mul_array = np.repeat(pattern[0:1], phase)
        else:
            mul_array = np.repeat(pattern, phase)

        if len(mul_array) < length+2:
            mul_array = np.tile(mul_array,int(length-len(mul_array))+2)[1:length+1]
        else:
            mul_array = mul_array[1:length+1]
        nums_aray= np.array([int(x) for x in nums])

        result = sum(np.multiply(mul_array,nums_aray))
        ret += str(result)[-1]

    return ret




def iterate_phases(nums,iterations):
    for i in range(iterations):
        nums = calc_phase(nums)
        if (i+1)%10 == 0:
            print (i)
    print (nums)
    return nums

def run_tests():
    assert iterate_phases("12345678",4) == "01029498"
    assert iterate_phases("80871224585914546619083218645595",100)[:8] == "24176176"
    assert iterate_phases("19617804207202209144916044189917",100)[:8] == "73745418"
    assert iterate_phases("69317163492948606335995924319873",100)[:8] == "52432133"

    print ("Tests passed")

if __name__ == '__main__':
    #run_tests()

    input = aoctools.get_input(16,2019)[0]
    offset = int(input[:7])

    #print("Solution for Puzzle 1: %s" %(iterate_phases(input,100)[:8]))
    print("Solution for Puzzle 2: %s" %(iterate_phases(input*10000,100)[offset:8+offset]))
