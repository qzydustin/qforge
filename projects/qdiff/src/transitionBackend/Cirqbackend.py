#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:03 PM
# @Author  : anonymous
# @File    : Cirqbackend.py

import re
import random

def simulator_to_same (address:str, iteration:int):
    writefile = open("../benchmark/startPyquil_QC" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()

    writefile_address = re.compile("../data/startPyquil")
    writefile_change = "../data/startCirq_Same"
    while line:
        n = writefile_address.search(line)
        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq_Same" + str(iteration) + ".py"

def simulator_to_pragma (address:str, iteration:int):#, clear_qubits:str):
    writefile = open("../benchmark/startCirq_pragma" + str(iteration) + ".py", "w")
    readfile = open(address)
    line = readfile.readline()

    clear_span = 1

    writefile_address = re.compile("../data/startCirq")
    writefile_change = "../data/startCirq_pragma"

    begin_optimizer = re.compile("import numpy as np")
    optimizer = "class Opty(cirq.PointOptimizer):\n" \
                "    def optimization_at(\n" \
                "            self,\n" \
                "            circuit: 'cirq.Circuit',\n" \
                "            index: int,\n" \
                "            op: 'cirq.Operation'\n" \
                "    ) -> Optional[cirq.PointOptimizationSummary]:\n" \
                "        if (isinstance(op, cirq.ops.GateOperation) and isinstance(op.gate, cirq.CZPowGate)):\n" \
                "            return cirq.PointOptimizationSummary(\n" \
                "                clear_span="+str(clear_span)+",\n" \
                "                clear_qubits=op.qubits, \n" \
                "                new_operations=[\n" \
                "                    cirq.CZ(*op.qubits),\n" \
                "                    cirq.X.on_each(*op.qubits),\n" \
                "                    cirq.X.on_each(*op.qubits),\n" \
                "                ]\n" \
                "            )\n"

    begin_run = re.compile("circuit_sample_count = 1024")

    while line:
        n = writefile_address.search(line)
        m = begin_optimizer.search(line)
        k = begin_run.search(line)

        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        elif m is not None:
            writefile.write(line)
            writefile.write(optimizer)
        elif k is not None:
            writefile.write(line)
            writefile.write("    Opty().optimize_circuit(circuit)\n")
        else:
            writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq_pragma" + str(iteration) + ".py"


def simulator_to_state_vector (address:str, iteration:int):
    pattern = re.compile("cirq.Simulator()")
    pattern1 = re.compile("simulator.run")  #find simulator

    writefile= open("../benchmark/startCirq_Class"+str(iteration)+".py", "w")
    writefile_address = re.compile("../data/startCirq")
    writefile_change = "../data/startCirq_Class"
    readfile = open(address)

    delete_measure = re.compile("cirq.measure")

    pattern_follow = re.compile("frequencies = result.histogram\(key='result', fold_func=bitstring\)")
    line = readfile.readline()
    while line:
        m = pattern.search(line)
        n = writefile_address.search(line)
        k = pattern_follow.search(line)

        skip_measure = delete_measure.search(line)
        if skip_measure is not None:
            line = readfile.readline()
            continue

        if m is not None:
            writefile.write("    info = cirq.final_state_vector(circuit)\n")
        elif n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        elif k is not None:
            writefile.write("    qubits = round(log2(len(info)))\n"
                            "    frequencies = {\n"
                            "        np.binary_repr(i, qubits): round((info[i]*(info[i].conjugate())).real,3)\n"
                            "        for i in range(2 ** qubits)\n"
                            "    }\n")
        else:
            if pattern1.search(line) is None:
                writefile.write(line)
        line = readfile.readline()

    writefile.close()
    readfile.close()
    return "startCirq_Class"+str(iteration)+".py"

def simulator_to_noisy (address:str, iteration:int):
    writefile = open("../benchmark/startCirq_noisy" + str(iteration) + ".py", "w")
    writefile_address = re.compile("../data/startCirq")
    writefile_change = "../data/startCirq_noisy"

    start_point = re.compile("simulator = cirq.Simulator()")
    readfile = open(address)
    line = readfile.readline()

    noisy = "    circuit = circuit.with_noise(cirq.depolarize(p=0.01))\n"
    while line:
        m = start_point.search(line)
        n = writefile_address.search(line)

        if n is not None:
            writefile.write(re.sub(writefile_address, writefile_change, line))
        elif m is not None:
            writefile.write(noisy)
            writefile.write(line)
        else:
            writefile.write(line)

        line = readfile.readline()


    writefile.close()
    readfile.close()
    return "startCirq_noisy" + str(iteration) + ".py"

def change_repetition  (address:str, repetition:int):

    readfile = open(address,"r")
    filedata =""

    repetition_find = re.compile("circuit_sample_count =")

    line = readfile.readline()
    while line:
        m = repetition_find.search(line)
        if m is not None:
            filedata += "    circuit_sample_count ="+str(repetition)+"\n"
        else:
            filedata += line

        line = readfile.readline()
    readfile.close()

    writefile = open(address,"w")
    writefile.write(filedata)
    writefile.close()

    return address



