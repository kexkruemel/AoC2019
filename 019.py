#!/usr/bin/env python3.5
from operator import add, mul
import aoctools
from termcolor import colored
from itertools import count

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
    code[get_parameter(code,modes,i,3)] = code[get_parameter(code,modes,i,1)] * code[get_parameter(code,modes,i,2)]
    return code,i+4,None

def _input(code,i,modes):
    code[get_parameter(code,modes,i,1)] =  prog_input
    if verbose:
        print ("Writing input %i to %i" %(prog_input,get_parameter(code,modes,i,1)))
    return code,i+2,None

def output(code,i,modes):
    ret = code[get_parameter(code,modes,i,1)]
    if verbose and ret not in [46,35,94,60,62,118,10]:
        print (colored("Output is %c -- %i" %(chr(ret),ret),"green"))
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


def run_program1(code):
    i = 0
    pos=0
    output_map = [[]]
    global prog_input

    while code[i] != 99:
        instruction="{:05d}".format(code[i])
        opcode = int(instruction[-2:])
        if opcode in [1,2,3,4,5,6,7,8,9]:
            op = (None,add,mul,_input,output,jump_if_true,jump_if_false,less_than,equal,adjust_base)[opcode]
            # if verbose:
            #     print(op.__name__, "- base is %i" %relative_base_offset)
            #     print_state(code,i)
            if step&verbose:
                input()
            if op == _input:
                prog_input = Instructions[pos]
                pos+=1
            code,i,ret = op(code,i,instruction[:-2])
        else:
            assert opcode[i] == 99, (code,i)
            break
    return ret

if __name__ == '__main__':
    prog_input = ""
    relative_base_offset = 0
    verbose = False
    step = False
    #run_tests()

    puzzle_input="109,424,203,1,21102,11,1,0,1106,0,282,21102,18,1,0,1106,0,259,1201,1,0,221,203,1,21102,31,1,0,1106,0,282,21101,38,0,0,1106,0,259,21002,23,1,2,22102,1,1,3,21101,1,0,1,21102,57,1,0,1105,1,303,2102,1,1,222,20101,0,221,3,20101,0,221,2,21102,259,1,1,21101,80,0,0,1106,0,225,21101,0,44,2,21102,91,1,0,1105,1,303,1201,1,0,223,20101,0,222,4,21101,0,259,3,21102,225,1,2,21101,225,0,1,21102,118,1,0,1105,1,225,21002,222,1,3,21101,100,0,2,21101,133,0,0,1105,1,303,21202,1,-1,1,22001,223,1,1,21101,148,0,0,1106,0,259,2102,1,1,223,20102,1,221,4,21002,222,1,3,21102,1,12,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,1,195,0,106,0,108,20207,1,223,2,21002,23,1,1,21102,-1,1,3,21101,0,214,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2102,1,-4,249,21201,-3,0,1,22101,0,-2,2,22101,0,-1,3,21101,0,250,0,1105,1,225,22102,1,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,21202,-2,1,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21101,0,343,0,1105,1,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21101,0,384,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,22102,1,1,-4,109,-5,2106,0,0"
    code_start = [int(x) for x in puzzle_input.split(",")]

    Instructions=[]
    sum = 0
    y_start = 0
    y_min = []
    y_max = []
    size = 1
    x= 0
    while 1:
        x+= 1
        #printstring = ""
        beam = False
        beam_finished = False
        for y in range(x):
            Instructions = [x,y]
            if y < y_start or beam_finished: #before and after beam
                #printstring += "."
                continue
            elif x>30 and beam and y < y_max[-1]: #middle of beam
                    #printstring += "#"
                    if x < 50 and y <50:
                        sum += 1
            else:
                ret = run_program1(code_start[:])
                if ret == 1:
                    if beam == False:
                        y_start = y
                        y_min.append(y)
                    #printstring += "#"
                    if x < 50 and y <50:
                        sum += 1
                    beam = True
                else:
                    #printstring += "."
                    if beam:
                        beam_finished = True
                        y_max.append(y-1)
        #printstring += " %i"%x
        #print(printstring)
        if x>10:
            if y_max[-size-1]-y_min[-1]>= size:
                print("Square of size %i at line %i" %(size+1,x))
                size += 1
        if size == 100:
            print(x,y_max[-1],y_min[-1])
            break


    print("Solution for Part1: %i" %sum)

    #print("Solution for Part2: %i" %run_program2(code_start[:]))
