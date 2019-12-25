#!/usr/bin/env python3.6

file_name = "001.txt"
file = open(file_name, 'r')

def calc_fuel(x):
    fuel = int(x/3) -2
    if fuel > 0:
        return fuel
    else:
        return 0

def calc_fuel_increment(x):
    x_sum = 0
    while x > 0:
        x = calc_fuel(x)
        x_sum += x
    return x_sum

def run_tests():
    assert calc_fuel(12) == 2
    assert calc_fuel(14) == 2
    assert calc_fuel(1969) == 654
    assert calc_fuel(100756) == 33583
    assert calc_fuel_increment(14) == 2
    assert calc_fuel_increment(1969) == 966
    assert calc_fuel_increment(100756) == 50346

if __name__ == '__main__':
    run_tests()
    print ("Tests passed")

    sum_1 = 0
    sum_2 = 0
    for line in file:
        sum_1 += calc_fuel(int(line))
        sum_2 += calc_fuel_increment(int(line))
    print ("Solution for puzzle 1: %i" %sum_1)
    print ("Solution for puzzle 1: %i" %sum_2)
