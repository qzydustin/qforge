#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 12:31 PM
# @Author  : anonymous
# @File    : Mutation_diff.py



import random
import re
from math import pi
gate_set_cirq = ["cirq.H","cirq.X","cirq.Y","cirq.Z","cirq.rx","cirq.CNOT","cirq.SWAP"]
gate_set_qiskit = ["prog.h","prog.x","prog.y","prog.z","prog.rx","prog.cx","prog.swap"]
gate_set_pyquil = ["prog += H(", "prog += X(","prog += Y(", "prog += Z(","prog += RX(", "prog += CNOT(", "prog += SWAP("]


def generate_same_add(address_in:str, address_out:str, add:str, total_number:int): # generate same mutation for pyquil and qiskit and cirq

    operation_find = re.compile("circuit end")
    total_operation_find = re.compile("total number")

    writefile_address = "../data/"+address_out[13:-3]+".csv"
    writefile_find = re.compile("../data/"+address_in[13:-3]+".csv")

    readfile = open(address_in)
    writefile = open(address_out,"w")
    line = readfile.readline()

    while line:

        if writefile_find.search(line):
            writefile.write(re.sub(writefile_find,writefile_address,line))
            line = readfile.readline()
            continue

        if operation_find.search(line):
            writefile.write(add+"\n"+line)
            line = readfile.readline()
            continue

        if total_operation_find.search(line):
            writefile.write("# total number="+str(total_number+1)+"\n")
        else:
            writefile.write(line)

        line = readfile.readline()

    readfile.close()
    writefile.close()


def mutate_add(tab:str, qubit_number:int, total_number:int):


    operation = 1

    qubit_on = 0
    qiskit_line = tab+gate_set_qiskit[operation]+"(input_qubit["+str(qubit_on)+"]) # number="+str(total_number)
    pyquil_line = tab + gate_set_pyquil[operation] + str(qubit_on) + ") # number=" + str(total_number)
    cirq_line = tab + "c.append(" + gate_set_cirq[operation] + ".on(input_qubit[" + str(qubit_on) + \
                    "])) # number=" + str(total_number)

    return cirq_line, qiskit_line, pyquil_line


def figure_out_tab (line:str):
    i = 0
    tab = ""
    while line[i] == " ":
        tab = tab + line[i]
        i = i + 1
    return tab

def mutate_start (address_in : str, seed:int, write:int):

    pyquil_address_in = "../benchmark/startPyquil"+ str(seed) + ".py"
    qiskit_address_in = "../benchmark/startQiskit"+ str(seed) + ".py"
    cirq_address_in = "../benchmark/startCirq"+ str(seed) + ".py"

    readfile = open(address_in)
    qubit_number_patter = re.compile("# qubit number=")
    total_operation_id = re.compile("# total number=")
    circuit_patter_end = re.compile("# circuit end")

    line = readfile.readline()
    qubit_number = 0
    total_number = 0
    while line:
        if figure_out_tab(line)!="":
            tab = figure_out_tab(line)

        if qubit_number_patter.search(line):
            qubit_number = int(line[qubit_number_patter.search(line).span()[1]:])

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:])

        if circuit_patter_end.search(line):
            if line!="\n":
                tab = figure_out_tab(line)
            cirq_line, qiskit_line, pyquil_line = mutate_add(tab, qubit_number, total_number)
            readfile.close()
            generate_same_add(pyquil_address_in, "../benchmark/startPyquil" + str(write) + ".py", pyquil_line,
                              total_number)
            generate_same_add(qiskit_address_in, "../benchmark/startQiskit" + str(write) + ".py", qiskit_line,
                              total_number)
            generate_same_add(cirq_address_in, "../benchmark/startCirq" + str(write) + ".py", cirq_line,
                              total_number)
            print("Must_Diff_Mutation" + str(write) + ":" + cirq_line)
            return 1

        line = readfile.readline()

    readfile.close()

    return 0




def mutate(seed : int, write : int, platform : str): # mutate and generate different program

    return  mutate_start("../benchmark/start"+platform+str(seed) + ".py", seed, write)

if __name__ == '__main__':
    mutate(11,12,"Cirq")