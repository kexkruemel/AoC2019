#!/usr/bin/env python3.5

def meets_criteria(no):
    if list(no) != sorted(no):
        return False
    return len(set(no)) != len(no)

def meets_criteria_2(no):
    if list(no) != sorted(no):
        return False
    return 2 in [str(no).count(j) for j in no] #check for doubles

def run_tests():
    assert meets_criteria("111111") == True
    assert meets_criteria("223450") == False
    assert meets_criteria("123789") == False
    assert meets_criteria_2("112233") == True
    assert meets_criteria_2("308800") == False
    assert meets_criteria_2("123444") == False
    assert meets_criteria_2("111122") == True

if __name__ == '__main__':
    run_tests()
    print ("Tests passed")

    input = range(128392,643281+1)

    sum_1 = 0
    sum_2 = 0
    for i in input:
        sum_1 += meets_criteria(str(i))
        sum_2 += meets_criteria_2(str(i))

    print("Solution for Puzle 1: %i " %sum_1)
    print("Solution for Puzle 2: %i " %sum_2)
