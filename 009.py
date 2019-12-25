#!/usr/bin/env python3.5
import sys
import unittest
from operator import add, mul
import aoctools
import datetime
from termcolor import colored

def check_size(code,dest):
    if dest > len(code):
        zeros = [0 for _ in range(dest-len(code)+2)]
        code += zeros
    return code

def add(code,i,modes):
    code = check_size(code,code[i+3])
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] + code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def mul(code,i,modes):
    code = check_size(code,code[i+3])
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] * code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def _input(code,i,modes):
    code = check_size(code,code[i+1])
    code[get_parameter(code,modes,i,1)] =  prog_input
    if verbose:
        print ("Writing input %i to %i" %(prog_input,get_parameter(code,modes,i,1)))
    return code,i+2,None

def output(code,i,modes):
    ret = code[get_parameter(code,modes,i,1)]
    print (colored("Output is %i" %ret,"green"))
    return code,i+2,ret

def jump_if_true(code,i,modes):
    pa1 = code[get_parameter(code,modes,i,1)]
    i = code[get_parameter(code,modes,i,2)] if pa1 else i+3
    return code,i,None

def jump_if_false(code,i,modes):
    i = code[get_parameter(code,modes,i,2)] if not code[get_parameter(code,modes,i,1)] else i+3
    return code,i,None

def less_than(code,i,modes):
    code = check_size(code,code[i+3])
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] < code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def equal(code,i,modes):
    code = check_size(code,code[i+3])
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] == code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def adjust_base(code,i,modes):
    global relative_base_offset
    relative_base_offset += code[get_parameter(code,modes,i,1)]
    return code,i+2,None

##################
def get_parameter(code,modes,i,pos):
    mode = modes[-pos]
    if mode == '1': # immediate mode
        code = check_size(code,i+pos)
        return i+pos
    elif mode == '0': # position mode
        code = check_size(code,code[i+pos])
        return code[i+pos]
    elif mode == '2': # relative mode
        code = check_size(code,code[i+pos] + relative_base_offset)
        return code[i+pos] + relative_base_offset
##################

def print_state(code,position):
    to_print = ["","",""]
    for i in range(len(code)):
        if i < position:
            to_print[0] += " %i" %code[i]
        elif i > position:
            to_print[2] += " %i" %code[i]
        else:
            to_print[1] += " %i" %code[i]
    print (to_print[0], colored(to_print[1], 'red'), to_print[2])


def run_program(code):
    i = 0
    instruction = 0
    while code[i] != 99:
        instruction="{:05d}".format(code[i])
        opcode = int(instruction[-2:])
        if opcode in [1,2,3,4,5,6,7,8,9]:
            op = (None,add,mul,_input,output,jump_if_true,jump_if_false,less_than,equal,adjust_base)[opcode]
            if verbose:
                print(op.__name__, "- base is %i" %relative_base_offset)
                print_state(code,i)
            if step&verbose:
                input()
            code,i,ret = op(code,i,instruction[:-2])
        else:
            assert opcode[i] == 99, (code,i)
            break
    #print (colored("Return is %i" %ret,"green"))
    return ret

def run_tests():
    assert run_program([104,1125899906842624,99]) == 1125899906842624
    assert run_program([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]) == None
    assert run_program([1102,34915192,34915192,7,4,7,99,0])

    print ("Tests passed")


if __name__ == '__main__':
    prog_input = 1
    relative_base_offset = 0
    verbose = False
    step = False
    #run_tests()

    code_start = [int(x) for x in aoctools.get_input(9,2019)[0].split(",")]

    print("Solution for Part1: %i" %run_program(code_start[:]))
    prog_input = 2
    relative_base_offset = 0
    print("Solution for Part2: %i" %run_program(code_start[:]))
