#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/31/20 8:49 PM
# @Author  : anonymous
# @File    : EqualT_breakdown.py

import re
from mutation.Mutation_equal import generate_same
import mutation.gateCirq_EqualT as MC
import mutation.gateQiskit_EqualT as MQ
import mutation.gatePyQuil_EqualT as MP
import mutation.TransformBack as Tr


#TODO: undone -> transform back



def generate_back():

    SS = Tr.TransformBack(2,['S','S'],['Z'])
    TT = Tr.TransformBack(2,['T','T'],['S'])
    HZH = Tr.TransformBack(2,['H','Z','H'],['X'])


    return 0

def generate_same_breakdown(operation_number:int, address_in:str, address_out:str, total_number:int, pattern:str, platform:str):

    operation_find = re.compile("# number="+str(operation_number)+"\n")
    writefile_address = "../data/"+address_out[13:-3]+".csv"
    writefile_find = re.compile("../data/"+address_in[13:-3]+".csv")
    total_operation_find = re.compile("# total number=")

    readfile = open(address_in)
    writefile = open(address_out,"w")
    line = readfile.readline()
    print("write at:",address_out)

    final_total = total_number

    while line:

        write_line=line
        if writefile_find.search(line):
            write_line = re.sub(writefile_find,writefile_address,write_line)
            writefile.write(write_line)
            line = readfile.readline()
            continue

        if operation_find.search(line):
            if platform=="Qiskit":
                if pattern == "SWAP":
                    write_line = MQ.swap_to_cnot(line, total_number)
                    final_total = final_total + 2
                if pattern == "Z":
                    write_line = MQ.z_to_s(line, total_number)
                    final_total = final_total + 1
                if pattern == "X":
                    write_line = MQ.x_to_hssh(line, total_number)
                    final_total = final_total + 3
                if pattern == "S":
                    write_line = MQ.s_to_t(line,total_number)
                    final_total = final_total + 1
            elif platform=="Cirq":
                if pattern == "SWAP":
                    write_line = MC.swap_to_cnot(line, total_number)
                    final_total = final_total + 2
                if pattern == "Z":
                    write_line = MC.z_to_cnotzcnot(line, total_number)
                    final_total = final_total + 1
                if pattern == "X":
                    write_line = MC.x_to_hssh(line, total_number)
                    final_total = final_total + 3
                if pattern == "S":
                    write_line = MC.s_to_t(line,total_number)
                    final_total = final_total + 1
            else:
                if pattern == "SWAP":
                    write_line = MP.swap_to_cnot(line, total_number)
                    final_total = final_total + 2
                if pattern == "Z":
                    write_line = MP.z_to_cnotzcnot(line, total_number)
                    final_total = final_total + 1
                if pattern == "X":
                    write_line = MP.x_to_hssh(line, total_number)
                    final_total = final_total + 3
                if pattern == "S":
                    write_line = MP.s_to_t(line,total_number)
                    final_total = final_total + 1

            writefile.write(write_line)
            line = readfile.readline()
            continue

        if total_operation_find.search(line):
            writefile.write("# total number="+str(final_total)+"\n") #update total operation number
        else:
            writefile.write(line)

        line = readfile.readline()

    writefile.close()
    readfile.close()


def breakdown(seed:int, write:int) -> int:


    cirq_address_in = "../benchmark/startCirq"+str(seed)+".py"
    pyquil_address_in = "../benchmark/startPyquil"+ str(seed) + ".py"
    qiskit_address_in = "../benchmark/startQiskit"+ str(seed) + ".py"

    cirq_address_out = "../benchmark/startCirq"+str(write)+".py"
    pyquil_address_out = "../benchmark/startPyquil"+ str(write) + ".py"
    qiskit_address_out = "../benchmark/startQiskit"+ str(write) + ".py"

    total_operation_id = re.compile("# total number=")
    operation_id = re.compile("# number=")

    readfile = open(cirq_address_in)
    line = readfile.readline()
    print("write at")

    patterns = {}
    patterns["SWAP"] = re.compile("cirq.SWAP")
    patterns["Z"] = re.compile("cirq.Z")
    patterns["X"] = re.compile("cirq.X")
    patterns["S"] = re.compile("cirq.S")

    while line:

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:len(line)-1])

        if operation_id.search(line):
            flag = int(line[operation_id.search(line).span()[1]:len(line)-1])

        for pattern in patterns:
            if patterns[pattern].search(line) and (operation_id.search(line) is not None):
                readfile.close()
                generate_same_breakdown(flag, cirq_address_in, cirq_address_out, total_number, pattern, "Cirq")
                generate_same_breakdown(flag, pyquil_address_in, pyquil_address_out, total_number, pattern, "Pyquil")
                generate_same_breakdown(flag, qiskit_address_in, qiskit_address_out, total_number, pattern, "Qiskit")
                return 0

        line = readfile.readline()
    readfile.close()


    return 1 # all possible transformation have been done

def breakdown_equal_transformation(seed:int, write:int) -> int:

    write_now = write
    flag = breakdown(seed, write_now)
    while flag != 1:
        write_now = write_now + 1
        flag = breakdown(seed, write_now) # execute all possible transformation

    return write_now-write # return how many programs we generate