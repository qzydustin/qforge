#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:17 PM
# @Author  : anonymous
# @File    : Pyquilbackend.py

import re
import random
pragma_pattern = ['NAIVE','PARTIAL','GREEDY']

def simulator_to_pragma (address:str, iteration:int):
    writefile = open("../benchmark/startPyquil_pragma" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()
    program_begin = re.compile("Program\(\)")
    i = random.randint(0,2)

    writefile_address = re.compile("../data/startPyquil")
    writefile_change = "../data/startPyquil_pragma"
    while line:
        n = writefile_address.search(line) # change writefile_address
        m = program_begin.search(line) # change pragma

        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        elif m is not None:
            writefile.write(re.sub(program_begin,'Program(\'PRAGMA INITIAL_REWIRING "'+pragma_pattern[i]+'"\')',line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startPyquil_pragma" + str(iteration) + ".py"

def simulator_to_Same (address:str, iteration:int):
    writefile = open("../benchmark/startPyquil_QC" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()

    writefile_address = re.compile("../data/startPyquil")
    writefile_change = "../data/startPyquil_Same"
    while line:
        n = writefile_address.search(line)
        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startPyquil_Same" + str(iteration) + ".py"


def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile("qvm")
    pattern_follow = re.compile("bitstrings =")
    pattern_follow2 = re.compile("print")

    writefile= open("../benchmark/startPyquil_Class"+str(iteration)+".py", "w")
    writefile_address = re.compile("../data/startPyquil")
    writefile_change = "../data/startPyquil_Class"

    readfile = open(address)
    line = readfile.readline()
    flag = 0
    while line:
        m = pattern.search(line)
        n = writefile_address.search(line)
        k = pattern_follow.search(line)
        z = pattern_follow2.search(line)
        if m is not None:
            if flag==0:
                writefile.write("    state = conn.wavefunction(prog)\n")
                flag=1
        elif n is not None:
            writefile.write(re.sub(writefile_address,writefile_change,line))
        elif z is not None:
            writefile.write("    print(state.get_outcome_probs(),file=writefile)\n")
        elif k is None:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startPyquil_Class" + str(iteration) + ".py"

def change_repetition (address:str, iteration:int):

    repetition_find = re.compile("qvm")
    readfile = open(address,"r")
    filedata=""

    line = readfile.readline()
    while line:
        m = repetition_find.search(line)

        if m is not None:
            filedata += "    results = qvm.run_and_measure(prog,"+str(iteration)+")\n"
        else:
            filedata += line
        line = readfile.readline()

    readfile.close()

    writefile = open(address,"w")
    writefile.write(filedata)
    writefile.close()