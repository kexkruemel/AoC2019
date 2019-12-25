#!/usr/bin/env python3.5
import sys
import unittest
from operator import add, mul
import aoctools
import datetime
import itertools
import numpy as np

def add(code,i,modes,inp):
    code[code[i+3]] = (get_parameter(code,modes,i,1) + get_parameter(code,modes,i,2))
    return code,i+4,None

def mul(code,i,modes,inp):
    code[code[i+3]] = (get_parameter(code,modes,i,1) * get_parameter(code,modes,i,2))
    return code,i+4,None

def input(code,i,modes,inp):
    code[code[i+1]] =  inp
    return code,i+2,None

def output(code,i,modes,inp):
    ret = get_parameter(code,modes,i,1)
    return code,i+2,ret

def jump_if_true(code,i,modes,inp):
    pa1 = get_parameter(code,modes,i,1)
    i = get_parameter(code,modes,i,2) if pa1 else i+3
    return code,i,None

def jump_if_false(code,i,modes,inp):
    i = get_parameter(code,modes,i,2) if not get_parameter(code,modes,i,1) else i+3
    return code,i,None

def less_than(code,i,modes,inp):
    code[code[i+3]] = (get_parameter(code,modes,i,1) < get_parameter(code,modes,i,2))
    return code,i+4,None

def equal(code,i,modes,inp):
    code[code[i+3]] = (get_parameter(code,modes,i,1) == get_parameter(code,modes,i,2))
    return code,i+4,None



def get_parameter(code,modes,i,pos):
    mode = modes[-pos]
    return code[i+pos] if mode == '1' else code[code[i+pos]] #immediate or parameter mode

def run_program(code,inputs):
    i = 0
    instruction = 0
    ret = 0
    curr_input = inputs[0]
    while code[i] != 99:
        instruction="{:05d}".format(code[i])
        opcode = int(instruction[-2:])
        if opcode in [1,2,3,4,5,6,7,8]:
            op = (None,add,mul,input,output,jump_if_true,jump_if_false,less_than,equal)[opcode]
            if op == input and i != 0:
                curr_input = inputs[1] # change to second input
            code,i,ret = op(code,i,instruction[:-2],curr_input)
            # if ret != None:
            #     print("Output is %i" %ret)
        else:
            assert opcode[i] == 99, (code,i)
            break
    return ret

def run_amplifiers1(code):
    phases = list(itertools.permutations([0,1,2,3,4]))

    max_ouput = 0
    max_phase=[]
    #phases = [[4,3,2,1,0]]
    for phase in phases:
        prog_input = 0
        for i in range(5):
            work_code = code[:]
            prog_input = run_program(work_code,[phase[i],prog_input])
        if prog_input > max_ouput:
            max_ouput = prog_input
            max_phase = phase[:]
    return max_ouput

def run_amplifiers2_for_phase(code,phase):

    work_codes = [code[:] for _ in range(5)]
    states = [0 for _ in range(5)]
    finished = [False for _ in range(5)]
    # go through all amplifiers one step
    phase = list(phase)
    signals = [np.NaN for _ in range(5)]
    signals[0] = 0
    output_e = np.NaN

    while 1:
        for amp in range(5):
            instruction="{:05d}".format(code[states[amp]])
            opcode = int(instruction[-2:])
            #print ("Working on instrucion %i of Amp %i" %(states[amp],amp))
            if opcode in [1,2,3,4,5,6,7,8]:
                do_compute = True
                op = (None,add,mul,input,output,jump_if_true,jump_if_false,less_than,equal)[opcode]
                if op == input:
                    if states[amp] == 0:
                        inp = phase[amp]
                        #print ("Amp %i uses phase %i" %(i,inp))
                    else:
                        inp = signals[amp]
                        if np.isnan(signals[amp]):
                            #print("Amp %i Waiting for input" %amp)
                            do_compute = False
                        else:
                            #print ("Amp %i has used %i" %(amp,inp))
                            signals[amp] = np.NaN
                if do_compute:
                    work_codes[amp],states[amp],ret = op(work_codes[amp],states[amp],instruction[:-2],inp)
                if op == output:
                    #print ("Amp %i has output %i" %(amp,ret))
                    signals[(amp+1)%5] = ret
                    if amp == 4:
                        output_e = ret

            else:
                assert opcode == 99
                #print ("Amp %i finished" %amp)
                if amp == 4:
                    return output_e


def run_amplifiers2(code):
    phases = list(itertools.permutations([5,6,7,8,9]))

    maximum = 0
    for phase in phases:
        ret = run_amplifiers2_for_phase(code,phase)
        maximum = max(maximum,ret)
    print(maximum)
    return maximum

def run_tests():
    #assert run_amplifiers1([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210
    #assert run_amplifiers1([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321
    #assert run_amplifiers1([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210
    assert run_amplifiers2([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]) == 139629729

if __name__ == '__main__':
    run_tests()
    print ("Tests passed")

    code_start = [int(x) for x in aoctools.get_input(7,2019)[0].split(",")]

    print("Solution for Part1: %i" %run_amplifiers1(code_start[:]))
    print("Solution for Part2: %i" %run_amplifiers2(code_start[:]))
