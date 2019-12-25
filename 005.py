#!/usr/bin/env python3.6
import sys
import unittest
from operator import add, mul
import aoctools
import datetime

def add(code,i,modes):
    code[code[i+3]] = (get_parameter(code,modes,i,1) + get_parameter(code,modes,i,2))
    return code,i+4

def mul(code,i,modes):
    code[code[i+3]] = (get_parameter(code,modes,i,1) * get_parameter(code,modes,i,2))
    return code,i+4

def input(code,i,modes):
    code[code[i+1]] =  prog_input
    return code,i+2

def output(code,i,modes):
    pa1 = get_parameter(code,modes,i,1)
    if pa1:
        if code[i+2]%100 != 99:
            print("Test failed at instruction %i" %i)
        else:
            print("Diagnostic Code is %i" %pa1)
    return code,i+2

def jump_if_true(code,i,modes):
    pa1 = get_parameter(code,modes,i,1)
    i = get_parameter(code,modes,i,2) if pa1 else i+3
    return code,i

def jump_if_false(code,i,modes):
    i = get_parameter(code,modes,i,2) if not get_parameter(code,modes,i,1) else i+3
    return code,i

def less_than(code,i,modes):
    code[code[i+3]] = (get_parameter(code,modes,i,1) < get_parameter(code,modes,i,2))
    return code,i+4

def equal(code,i,modes):
    code[code[i+3]] = (get_parameter(code,modes,i,1) == get_parameter(code,modes,i,2))
    return code,i+4

def get_parameter(code,modes,i,pos):
    mode = modes[-pos]
    return code[i+pos] if mode == '1' else code[code[i+pos]] #immediate or parameter mode

def run_program(code):
    i = 0
    instruction = 0
    while code[i] != 99:
        instruction=f"{code[i]:05}"
        opcode = int(instruction[-2:])
        if opcode in [1,2,3,4,5,6,7,8]:
            op = (None,add,mul,input,output,jump_if_true,jump_if_false,less_than,equal)[opcode]
            code,i = op(code,i,instruction[:-2])
        else:
            assert opcode[i] == 99, (code,i)
            break
    return code[0]

def run_tests():
    assert run_program([1,9,10,3,2,3,11,0,99,30,40,50]) == 3500
    assert run_program([1,0,0,0,99]) == 2
    assert run_program([2,3,0,3,99]) == 2
    assert run_program([2,4,4,5,99,0]) == 2
    assert run_program([1,1,1,4,99,5,6,0,99]) == 30
    assert run_program([3,0,4,0,99])
    assert run_program([3,9,8,9,10,9,4,9,99,-1,8])
    assert run_program([3,9,7,9,10,9,4,9,99,-1,8])
    assert run_program([3,3,1108,-1,8,3,4,3,99])
    assert run_program([3,3,1107,-1,8,3,4,3,99])
    assert run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
    assert run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
    assert run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])


if __name__ == '__main__':
    prog_input = 1
    run_tests()
    print ("Tests passed")

    code_start = [int(x) for x in aoctools.get_input(5,2019)[0].split(",")]

    start = datetime.datetime.now()
    prog_input = 1
    run_program(code_start[:])
    S1 = datetime.datetime.now()
    print ("Took %s sec" %str(S1-start))
    prog_input = 5
    run_program(code_start[:])
    S2 = datetime.datetime.now()
    print ("Took %s sec" %str(S2-S1))
