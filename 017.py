#!/usr/bin/env python3.5
import sys
import unittest
from operator import add, mul
import aoctools
import datetime
from termcolor import colored

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
            code,i,ret = op(code,i,instruction[:-2])
            if op == output:
                if ret == 10:
                    output_map.append([])
                else:
                    output_map[-1] += chr(ret)
        else:
            assert opcode[i] == 99, (code,i)
            break
    return output_map

def run_program2(code):
    i = 0
    Instructions = "A,A,C,B,B,A,B,C,B,C-L,4,L,4,L,6,R,10,L,6-R,8,R,10,L,6-L,12,L,6,R,10,L,6-n-"
    output_map=[[]]
    pos = 0

    while code[i] != 99:
        global prog_input
        instruction="{:05d}".format(code[i])
        opcode = int(instruction[-2:])
        if opcode in [1,2,3,4,5,6,7,8,9]:
            op = (None,add,mul,_input,output,jump_if_true,jump_if_false,less_than,equal,adjust_base)[opcode]
            if op == _input:
                #if verbose:
                #    print(op.__name__, "- base is %i" %relative_base_offset)
                #    print_state(code,i)
                if step&verbose:
                    input()
                if Instructions[pos] == "-":
                    if verbose: print("Inputting %c  --   %i" %(" ",10))
                    prog_input = 10
                else:
                    if verbose: print("Inputting %c  --   %i" %(Instructions[pos],ord(Instructions[pos])))
                    prog_input = ord(Instructions[pos])
                pos += 1

            code,i,ret = op(code,i,instruction[:-2])


            if op == output:
                if ret > 126:
                    print(colored("Returned %i" %ret, color='yellow'))
                elif ret == 10:
                    output_map.append([])
                else:
                    output_map[-1] += chr(ret)
        else:
            assert opcode[i] == 99, (code,i)
            break
    return output_map

def calc_junctions(scaffold_map):
    par_sum = 0
    for i in range(1,len(scaffold_map[0])-2):
        for j in range(1,len(scaffold_map)-2):
            #print(len(scaffold_map[0]),len(scaffold_map),i,j)
            if (scaffold_map[j][i] == "#") and (scaffold_map[j-1][i] == "#") and (scaffold_map[j+1][i] == "#") and (scaffold_map[j][i-1] == "#") and (scaffold_map[j][i+1] == "#"):
                print ("Found junction at [%i,%i]" %(i,j))
                par_sum += i*j
    return par_sum

def run_tests():
    assert run_program([104,1125899906842624,99]) == 1125899906842624
    assert run_program([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]) == None
    assert run_program([1102,34915192,34915192,7,4,7,99,0])

    print ("Tests passed")

def print_scaffold(scaffold_map):
    for row in scaffold_map:
        row_char = ""
        for item in row:
            row_char += str(item)
        print(row_char)


if __name__ == '__main__':
    prog_input = 1
    relative_base_offset = 0
    verbose = False
    step = False
    #run_tests()

    puzzle_input="1,330,331,332,109,3016,1101,1182,0,16,1101,1441,0,24,102,1,0,570,1006,570,36,1002,571,1,0,1001,570,-1,570,1001,24,1,24,1106,0,18,1008,571,0,571,1001,16,1,16,1008,16,1441,570,1006,570,14,21101,58,0,0,1105,1,786,1006,332,62,99,21101,333,0,1,21101,73,0,0,1105,1,579,1101,0,0,572,1101,0,0,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,102,1,574,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1106,0,81,21101,340,0,1,1106,0,177,21102,1,477,1,1106,0,177,21101,514,0,1,21102,176,1,0,1105,1,579,99,21102,1,184,0,1105,1,579,4,574,104,10,99,1007,573,22,570,1006,570,165,1002,572,1,1182,21101,0,375,1,21101,211,0,0,1105,1,579,21101,1182,11,1,21101,222,0,0,1105,1,979,21102,1,388,1,21102,1,233,0,1105,1,579,21101,1182,22,1,21102,244,1,0,1106,0,979,21102,401,1,1,21101,0,255,0,1106,0,579,21101,1182,33,1,21101,266,0,0,1106,0,979,21102,414,1,1,21101,0,277,0,1105,1,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21102,1,1182,1,21101,0,313,0,1106,0,622,1005,575,327,1102,1,1,575,21101,327,0,0,1106,0,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,14,0,0,109,4,1202,-3,1,587,20102,1,0,-1,22101,1,-3,-3,21102,0,1,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1105,1,597,109,-4,2105,1,0,109,5,1202,-4,1,630,20101,0,0,-2,22101,1,-4,-4,21102,0,1,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,652,21002,0,1,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21101,0,702,0,1106,0,786,21201,-1,-1,-1,1105,1,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21101,0,731,0,1105,1,786,1105,1,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21101,756,0,0,1106,0,786,1105,1,774,21202,-1,-11,1,22101,1182,1,1,21101,774,0,0,1106,0,622,21201,-3,1,-3,1105,1,640,109,-5,2106,0,0,109,7,1005,575,802,20101,0,576,-6,20101,0,577,-5,1106,0,814,21101,0,0,-1,21101,0,0,-5,21102,1,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,45,-3,22201,-6,-3,-3,22101,1441,-3,-3,2101,0,-3,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21102,1,1,-1,1105,1,924,1205,-2,873,21101,35,0,-4,1106,0,924,1201,-3,0,878,1008,0,1,570,1006,570,916,1001,374,1,374,1202,-3,1,895,1101,2,0,0,1201,-3,0,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,922,20101,0,0,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,45,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,35,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1101,0,1,575,21101,973,0,0,1105,1,786,99,109,-7,2106,0,0,109,6,21102,0,1,-4,21102,1,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1105,1,1041,21102,-4,1,-2,1105,1,1041,21101,-5,0,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,1202,-2,1,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,2101,0,-2,0,1106,0,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1106,0,989,21102,439,1,1,1105,1,1150,21102,477,1,1,1106,0,1150,21101,514,0,1,21102,1149,1,0,1105,1,579,99,21101,1157,0,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,2101,0,-5,1176,2101,0,-4,0,109,-6,2106,0,0,10,5,40,1,44,1,44,1,44,7,44,1,44,1,7,13,24,1,7,1,11,1,8,7,9,1,7,1,11,1,8,1,5,1,9,1,7,1,11,1,8,1,5,1,9,1,1,5,1,1,5,9,6,1,5,1,9,1,1,1,3,1,1,1,5,1,5,1,1,1,6,1,5,1,7,11,1,11,1,1,6,1,5,1,7,1,1,1,1,1,3,1,3,1,3,1,7,1,6,1,5,1,7,1,1,7,3,1,3,1,7,1,6,1,5,1,7,1,3,1,7,1,3,1,7,1,6,1,5,1,1,11,1,11,7,1,6,1,5,1,1,1,5,1,5,1,5,1,11,1,6,1,5,9,5,1,5,1,11,1,6,1,7,1,11,1,5,1,11,1,6,7,1,1,11,1,5,7,5,7,6,1,1,1,11,1,11,1,11,1,6,1,1,13,11,1,11,1,6,1,25,1,11,1,6,1,25,1,11,1,6,1,25,1,11,1,6,1,25,1,11,1,6,1,25,1,11,1,6,1,25,1,1,11,6,1,25,1,1,1,16,7,19,7,40,1,3,1,40,1,3,1,40,1,3,1,40,5,6"

    code_start = [int(x) for x in puzzle_input.split(",")]
    # scaffold_map = run_program1(code_start[:])
    # scaffold_map = scaffold_map[:-2]
    # print_scaffold(scaffold_map)
    #
    # print("Solution for Part1: %i" %calc_junctions(scaffold_map))
    code_start = [int(x) for x in aoctools.get_input(17,2019)[0].split(",")]

    code_start[0] = 2
    scaffold_map = run_program2(code_start[:])
    scaffold_map = scaffold_map[:-2]
    print_scaffold(scaffold_map)
    #relative_base_offset = 0
    #print("Solution for Part2: %i" %run_program2(code_start[:]))
