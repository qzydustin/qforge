#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/20/20 8:07 PM
# @Author  : anonymous
# @File    : Mutation_equal.py

#TODO:integrate transformation rules

import re
import random
import mutation.gateCirq_EqualT as MC
import mutation.gateQiskit_EqualT as MQ
import mutation.gatePyQuil_EqualT as MP

def figure_out_tab (line:str):
    i = 0
    tab = ""
    while line[i] == " ":
        tab = tab + line[i]
        i = i + 1
    return tab


def generate_trival(address_in:str, address_out:str, total_number:int,platform:str,qubit_number:int, mutation_number:int): # generate two X/Y/CNOT gate?

    end_find = re.compile("# circuit end")
    writefile_address = "../data/"+address_out[13:-3]+".csv"
    writefile_find = re.compile("../data/"+address_in[13:-3]+".csv")
    total_operation_find = re.compile("# total number=")

    readfile = open(address_in)
    writefile = open(address_out,"w")
    line = readfile.readline()
    print("write at:", address_out)


    equal_change = ["X","Y","SWAP","CNOT"]
    pattern = equal_change[mutation_number]


    tab = ""

    while line:

        if figure_out_tab(line)!="":
            tab = figure_out_tab(line)

        write_line = line
        if writefile_find.search(line):
            write_line = re.sub(writefile_find, writefile_address, write_line) #change write file in program
            writefile.write(write_line)
            line = readfile.readline()
            continue

        if end_find.search(line):
            if platform == "Qiskit":
                if pattern == "CNOT":
                    if qubit_number==0:
                        write_line = MQ.two_CNOT(tab, 1, total_number)
                    else:
                        write_line = MQ.two_CNOT(tab, qubit_number,total_number)
                if pattern == "SWAP":
                    if qubit_number==0:
                        write_line = MQ.two_SWAP(tab, 1, total_number)
                    else:
                        write_line = MQ.two_SWAP(tab, qubit_number,total_number)
                if pattern == "Y":
                    write_line = MQ.two_Y(tab, qubit_number,total_number)
                if pattern == "X":
                    write_line = MQ.two_X(tab, qubit_number,total_number)
            elif platform == "Cirq":
                if pattern == "CNOT":
                    if qubit_number==0:
                        write_line = MC.two_CNOT(tab, 1, total_number)
                    else:
                        write_line = MC.two_CNOT(tab, qubit_number,total_number)
                if pattern == "SWAP":
                    if qubit_number==0:
                        write_line = MC.two_SWAP(tab, 1, total_number)
                    else:
                        write_line = MC.two_SWAP(tab, qubit_number,total_number)
                if pattern == "Y":
                    write_line = MC.two_Y(tab, qubit_number,total_number)
                if pattern == "X":
                    write_line = MC.two_X(tab, qubit_number,total_number)
            else:
                if pattern == "CNOT":
                    if qubit_number==0:
                        write_line = MP.two_CNOT(tab, 1, total_number)
                    else:
                        write_line = MP.two_CNOT(tab, qubit_number,total_number)
                if pattern == "SWAP":
                    if qubit_number==0:
                        write_line = MP.two_SWAP(tab, 1, total_number)
                    else:
                        write_line = MP.two_SWAP(tab, qubit_number,total_number)
                if pattern == "Y":
                    write_line = MP.two_Y(tab, qubit_number,total_number)
                if pattern == "X":
                    write_line = MP.two_X(tab, qubit_number,total_number)

            write_line = write_line+line

            writefile.write(write_line)
            line = readfile.readline()
            continue

        if total_operation_find.search(line):
            writefile.write("# total number=" + str(total_number + 2) + "\n")  # update total operation number
        else:
            writefile.write(line)

        line = readfile.readline()

    writefile.close()
    readfile.close()






def generate_same(operation_number:int, address_in:str, address_out:str, total_number:int, pattern:str, platform:str):

    operation_find = re.compile("# number="+str(operation_number)+"\n")
    writefile_address = "../data/"+address_out[13:-3]+".csv"
    writefile_find = re.compile("../data/"+address_in[13:-3]+".csv")
    total_operation_find = re.compile("# total number=")

    readfile = open(address_in)
    writefile = open(address_out,"w")
    line = readfile.readline()
    print("write at:",address_out)

    while line:

        write_line=line
        if writefile_find.search(line):
            write_line = re.sub(writefile_find,writefile_address,write_line)
            writefile.write(write_line)
            line = readfile.readline()
            continue

        if operation_find.search(line):
            if platform=="Qiskit":
                if pattern == "CNOT":
                    write_line = MQ.cnot_to_hczh(line, total_number)
                if pattern == "Z":
                    write_line = MQ.z_to_cnotzcnot(line, total_number)
                if pattern == "X":
                    write_line = MQ.x_to_cnotxcnot(line, total_number)
            elif platform=="Cirq":
                if pattern == "CNOT":
                    write_line = MC.cnot_to_hczh(line, total_number)
                if pattern == "Z":
                    write_line = MC.z_to_cnotzcnot(line, total_number)
                if pattern == "X":
                    write_line = MC.x_to_cnotxcnot(line, total_number)
            else:
                if pattern == "CNOT":
                    write_line = MP.cnot_to_hczh(line, total_number)
                if pattern == "Z":
                    write_line = MP.z_to_cnotzcnot(line, total_number)
                if pattern == "X":
                    write_line = MP.x_to_cnotxcnot(line, total_number)

            writefile.write(write_line)
            line = readfile.readline()
            continue

        if total_operation_find.search(line):
            writefile.write("# total number="+str(total_number+3)+"\n") #update total operation number
        else:
            writefile.write(line)

        line = readfile.readline()

    writefile.close()
    readfile.close()



def mutate(seed:int, write:int):

    qubit_number_patter = re.compile("# qubit number=")
    total_operation_id = re.compile("# total number=")
    operation_id = re.compile("# number=")
    patterns = {}

    patterns["CNOT"] = re.compile("cirq.CNOT")
    patterns["Z"] = re.compile("cirq.Z")
    patterns["X"] = re.compile("cirq.X")

    circuit_patter_end = re.compile("# circuit end")

    total_number=0
    flag=0 # To check if enter the circuit code or not
    qubit_number=0 # To find the total qubit number

    cirq_address_in = "../benchmark/startCirq"+str(seed)+".py"
    pyquil_address_in = "../benchmark/startPyquil"+ str(seed) + ".py"
    qiskit_address_in = "../benchmark/startQiskit"+ str(seed) + ".py"
    readfile = open(cirq_address_in)
    line = readfile.readline()

    cirq_address_out = "../benchmark/startCirq"+str(write)+".py"
    pyquil_address_out = "../benchmark/startPyquil"+ str(write) + ".py"
    qiskit_address_out = "../benchmark/startQiskit"+ str(write) + ".py"
    while line:

        if total_operation_id.search(line):
            total_number = int(line[total_operation_id.search(line).span()[1]:len(line)-1])

        if qubit_number_patter.search(line):
            qubit_number = int(line[qubit_number_patter.search(line).span()[1]:])

        if operation_id.search(line):
            flag = int(line[operation_id.search(line).span()[1]:len(line)-1])

        for pattern in patterns:
            if (patterns[pattern].search(line) is not None) and (operation_id.search(line) is not None) and (qubit_number>1):
                if random.randint(0,5)>3 :

                    readfile.close()
                    generate_same(flag, cirq_address_in, cirq_address_out, total_number, pattern, "Cirq")
                    generate_same(flag, pyquil_address_in, pyquil_address_out, total_number, pattern, "Pyquil")
                    generate_same(flag, qiskit_address_in, qiskit_address_out, total_number, pattern, "Qiskit")
                    return

        if circuit_patter_end.search(line) is not None:
            mutate_qubit_number = random.randint(0,qubit_number-1) # the qubit that mutate operation on
            mutation_number = random.randint(0,3)  #right now we have four trivial mutation way
            if qubit_number==1:
                mutation_number = random.randint(0,1)
            generate_trival(cirq_address_in,cirq_address_out,total_number,"Cirq",mutate_qubit_number,mutation_number)
            generate_trival(pyquil_address_in,pyquil_address_out,total_number,"Pyquil",mutate_qubit_number,mutation_number)
            generate_trival(qiskit_address_in,qiskit_address_out,total_number,"Qiskit",mutate_qubit_number,mutation_number)
            return
        line = readfile.readline()

    readfile.close()
