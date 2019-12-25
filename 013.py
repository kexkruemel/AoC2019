#!/usr/bin/env python3.5
import sys
import unittest
import aoctools
import datetime
from termcolor import colored
from collections import defaultdict
import time

paint_instr= {  0 : ' ',
                1 : '#',
                2 : '.',
                3 : '_',
                4 : 'o'}

def check_size(code,dest):
    if dest >= len(code):
        zeros = [0 for _ in range(dest-len(code)+2)]
        code += zeros
    return code

#############
def add(code,i,modes):
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] + code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def mul(code,i,modes):
    #code = check_size(code,get_parameter(code,modes,i,3))
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] * code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def _input(code,i,modes):
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
    #print_state(code,i)
    #print("positions: %i,%i" %(get_parameter(code,modes,i,1),get_parameter(code,modes,i,2)))
    #print("values at positions: %i,%i" %(code[get_parameter(code,modes,i,1)],code[get_parameter(code,modes,i,2)]))
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] < code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def equal(code,i,modes):
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

def paint_game(panels):
    if len(panels) > 0:
        size_x_min= min([x[1] for x in panels])
        size_y_min= min([x[0] for x in panels])
        size_x_max= max([x[1] for x in panels])
        size_y_max= max([x[0] for x in panels])

        for x in range(size_x_min,size_x_max+1):
            printstring = ""
            for y in range(size_y_min,size_y_max+1):
                printstring += paint_instr[panels[(y,x)]]
            print (printstring)
    print(end='\r')


def run_program(code,part):
    global prog_input
    if part == 2:
        code[0] = 2
    panels = defaultdict(int)
    pos = [0,0]
    ball_pos = []
    paddle_pos = []
    type = 0 # 0 -> x pos; 1-> y pos; 3 -> paint
    i = 0

    while code[i] != 99:
        instruction="{:05d}".format(code[i])
        opcode = int(instruction[-2:])
        if opcode in [1,2,3,4,5,6,7,8,9]:
            op = (None,add,mul,_input,output,jump_if_true,jump_if_false,less_than,equal,adjust_base)[opcode]
            if op == _input:
                # do something with input
                if part == 1:
                    continue
                if part == 2: #move joystick
                    if watch:
                        paint_game(panels)
                        print ("Score is %i" %score)
                        time.sleep(0.1)
                    if paddle_pos[0] < ball_pos[0]:
                        prog_input = +1
                    elif paddle_pos[0] > ball_pos[0]:
                        prog_input = -1
                    else:
                        prog_input = 0

            if verbose:
                print(op.__name__, "- base is %i" %relative_base_offset)
                print("Position is %str" %(str(pos)))
                #print_state(code,i)
            code,i,ret = op(code,i,instruction[:-2])
            if op == output:
                if type == 0:
                    pos[0]=ret
                elif type == 1:
                    pos[1]=ret
                elif type == 2:
                    if pos == [-1,0]:
                        score = ret
                    else:
                        panels[tuple(pos)] = ret # add to panels
                        if ret == 4:
                            ball_pos = pos[:]
                        elif ret == 3:
                            paddle_pos = pos[:]
                        if verbose and step:
                            input()

                type = (type+1)%3
        else:
            assert opcode[i] == 99, (code,i)
            break
    #print (colored("Return is %i" %ret,"green"))
    summe = sum([1 for key in panels if panels[key] == 2])
    paint_game(panels)
    if part ==1:
        return summe
    else:
        return score


if __name__ == '__main__':
    prog_input = None
    relative_base_offset = 0
    verbose = False
    step = False
    watch = True


    code_start = [int(x) for x in aoctools.get_input(13,2019)[0].split(",")]

    #print("Solution for Part1: %i" %run_program(code_start[:],1))

    print("Solution for Part2: %i" %run_program(code_start[:],2))
