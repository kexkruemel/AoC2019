#!/usr/bin/env python3.5
import sys
import unittest
from operator import add, mul
import aoctools
import datetime
from termcolor import colored
from collections import defaultdict

movements = {"D" : [+1,0],
              "U" : [-1,0],
              "R" : [0,+1],
              "L" : [0,-1]}

turn_right = {"D" : "L",
              "U" : "R",
              "R" : "D",
              "L" : "U"}
turn_left =  {"D" : "R",
              "U" : "L",
              "R" : "U",
              "L" : "D"}

def check_size(code,dest):
    if dest >= len(code):
        zeros = [0 for _ in range(dest-len(code)+2)]
        code += zeros
    return code

def add(code,i,modes):
    #code = check_size(code,get_parameter(code,modes,i,3))
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] + code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def mul(code,i,modes):
    #code = check_size(code,get_parameter(code,modes,i,3))
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] * code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def _input(code,i,modes):
    #code = check_size(code,get_parameter(code,modes,i,1))
    code[get_parameter(code,modes,i,1)] =  prog_input
    if verbose:
        print ("Writing input %i to %i" %(prog_input,get_parameter(code,modes,i,1)))
    return code,i+2,None

def output(code,i,modes):
    ret = code[get_parameter(code,modes,i,1)]
    if verbose: print (colored("Output is %i" %ret,"green"))
    return code,i+2,ret

def jump_if_true(code,i,modes):
    pa1 = code[get_parameter(code,modes,i,1)]
    i = code[get_parameter(code,modes,i,2)] if pa1 else i+3
    return code,i,None

def jump_if_false(code,i,modes):
    i = code[get_parameter(code,modes,i,2)] if not code[get_parameter(code,modes,i,1)] else i+3
    return code,i,None

def less_than(code,i,modes):
    #code = check_size(get_parameter(code,modes,i,3))
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] < code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def equal(code,i,modes):
    #code = check_size(get_parameter(code,modes,i,3))
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

def paint_canvas(panels):
    if len(panels) > 0:
        size_x_min= min([x[1] for x in panels])
        size_y_min= min([x[0] for x in panels])
        size_x_max= max([x[1] for x in panels])
        size_y_max= max([x[0] for x in panels])

        for y in range(size_y_min,size_y_max+1):
            printstring = ""
            for x in range(size_x_min,size_x_max+1):
                if panels[(y,x)] == 1: printstring += "#"
                else: printstring += "."
            print (printstring)

def run_program(code,start_color):
    global prog_input
    panels = defaultdict(int)
    i = 0
    instruction = 0
    dir = 'U'
    pos = [0,0]
    turn = False
    panels[(0,0)] = start_color

    while code[i] != 99:
        instruction="{:05d}".format(code[i])
        opcode = int(instruction[-2:])
        if opcode in [1,2,3,4,5,6,7,8,9]:
            op = (None,add,mul,_input,output,jump_if_true,jump_if_false,less_than,equal,adjust_base)[opcode]
            if op == _input:
                # provide 0 if the robot is over a black panel
                # or 1 if the robot is over a white panel
                prog_input = panels[tuple(pos)]
            # if verbose:
            #     print(op.__name__, "- base is %i" %relative_base_offset)
            #     print("Position is %str, facing %c" %(str(pos),dir))
            #     print_state(code,i)
            # if step&verbose:
            #     input()
            code,i,ret = op(code,i,instruction[:-2])
            if op == output:
                if turn: #means it has to turn
                # 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
                    if ret == 0:
                        dir = turn_left[dir]
                    else:
                        dir = turn_right[dir]
                    #After the robot turns, it should always move forward exactly one panel. The robot starts facing up.
                    pos[0] += movements[dir][0]
                    pos[1] += movements[dir][1]
                    turn = False
                    if verbose:
                        print("Position: " +str(pos))
                        print("Direction: " +str(dir))
                        paint_canvas(panels)
                else: #mean it has to paint
                # 0 means to paint the panel black, and 1 means to paint the panel white.
                    panels[tuple(pos)] = ret
                    turn = True #after paining turn
                    if verbose:
                        print("Position: " +str(pos))
                        paint_canvas(panels)
                if step: input()

        else:
            assert opcode[i] == 99, (code,i)
            break
    #print (colored("Return is %i" %ret,"green"))
    size = len(panels)
    paint_canvas(panels)
    return size


if __name__ == '__main__':
    prog_input = None
    relative_base_offset = 0
    verbose = False
    step = False


    code_start = [int(x) for x in aoctools.get_input(11,2019)[0].split(",")]

    print("Solution for Part1: %i" %run_program(code_start[:],0))
    prog_input = None
    relative_base_offset = 0

    print("Solution for Part2: %i" %run_program(code_start[:],1))
