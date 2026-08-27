#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/26/20 10:09 PM
# Quantum transformation rules
# @File    : MutateCirq_equal.py

#TODO: test transformation

import re

def cnot_to_hczh(codeline:str, number:int):
    if re.search('cirq.CNOT', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]","",codeline)
        return re.sub(r'cirq.CNOT.on[(](.*)[,]', "cirq.H.on(", new_codeline)+"# number="+str(number)+"\n"+ \
               re.sub('cirq.CNOT', "cirq.CZ", new_codeline)+"# number="+str(number+1)+"\n"+ \
               re.sub(r'cirq.CNOT.on[(](.*)[,]',"cirq.H.on(", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No CNOT gate for CZ transformation')

def cz_to_hconth(codeline:str, number:int):
    if re.search('cirq.CZ', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]","",codeline)
        return re.sub(r'cirq.CZ.on[(](.*)[,]', "cirq.H.on(", new_codeline)+"# number="+str(number)+"\n"+ \
               re.sub('cirq.CZ', "cirq.CNOT", new_codeline)+"# number="+str(number+1)+"\n"+ \
               re.sub(r'cirq.CZ.on[(](.*)[,]',"cirq.H.on(", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No CZ gate for CNOT transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str,number:int):
    if re.search('cirq.SWAP', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('cirq.SWAP', 'cirq.CNOT', new_codeline)+"# number="+str(number)+"\n"+\
               re.sub('cirq.SWAP', "cirq.CNOT", new_codeline)+"# number="+str(number+1)+"\n"+\
               re.sub('cirq.SWAP',"cirq.CNOT", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str,number:int):

    help_qubit_now = re.compile("cirq.X.on[(]input_qubit[[]")
    help_qubit = int(codeline[help_qubit_now.search(codeline).span()[1]]) #can not handle 10+ qubits
    if help_qubit==0:
        help_qubit = 1
    else:
        help_qubit = 0
    if re.search('cirq.X', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub(r'cirq.X.on[(]', "cirq.CNOT.on(input_qubit["+str(help_qubit)+"],", new_codeline)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'cirq.X.on[(]', "cirq.CNOT.on(input_qubit["+str(help_qubit)+"],", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str,number:int):
    new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
    if re.search('cirq.Z', codeline) is not None:

        help_qubit_now = re.compile("cirq.Z.on[(]input_qubit[[]")
        help_qubit = int(codeline[help_qubit_now.search(codeline).span()[1] ])  # can not handle 10+ qubits
        if help_qubit == 0:
            help_qubit = 1
        else:
            help_qubit = 0

        codeline1 = re.sub(r'cirq.Z', "cirq.CNOT", new_codeline)
        return re.sub(r'[)]', ",input_qubit["+str(help_qubit)+"])", codeline1,count=1)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'[)]', ",input_qubit["+str(help_qubit)+"])", codeline1,count=1)+"# number="+str(number+2)+"\n"
    else:
        print(codeline)
        raise Exception('No Z gate for Z transformation')

def two_X(tab:str,qubit_number:int, number:int):
    return tab+"c.append(cirq.X.on(input_qubit["+str(qubit_number)+"]))"+" # number="+str(number)+"\n"+\
           tab+"c.append(cirq.X.on(input_qubit["+str(qubit_number)+"]))"+" # number="+str(number+1)+"\n"

def two_Y(tab:str, qubit_number:int, number:int):
    return tab+"c.append(cirq.Y.on(input_qubit[" + str(qubit_number) + "]))" + " # number=" + str(number) + "\n" + \
           tab+"c.append(cirq.Y.on(input_qubit[" + str(qubit_number) + "]))" + " # number=" + str(number + 1) + "\n"

def two_CNOT(tab:str,qubit_number:int, number:int):
    return tab+"c.append(cirq.CNOT.on(input_qubit[" + str(qubit_number) + "],input_qubit[0]))" + " # number=" + str(number) + "\n" + \
           tab+"c.append(cirq.CNOT.on(input_qubit[" + str(qubit_number) + "],input_qubit[0]))" + " # number=" + str(number + 1) + "\n"

def two_SWAP(tab:str, qubit_number:int, number:int):
    return tab + "c.append(cirq.SWAP.on(input_qubit[" + str(qubit_number) + "],input_qubit[0]))" + " # number=" + str(
        number) + "\n" + \
           tab + "c.append(cirq.SWAP.on(input_qubit[" + str(qubit_number) + "],input_qubit[0]))" + " # number=" + str(
        number + 1) + "\n"

def s_to_t(codeline:str,number:int):
    if re.search('criq.S',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('cirq.S', "cirq.T", new_codeline) + "# number=" + str(number) + "\n" + \
               re.sub('cirq.S', "cirq.T", new_codeline) + "# number=" + str(number + 1) + "\n"
    else:
        raise Exception('No S gate for T transformation')

def z_to_s(codeline:str,number:int):
    if re.search('cirq.Z',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline = re.sub(r'cirq.Z',"cirq.S",new_codeline)+"# number="+str(number)+"\n"+\
                   re.sub(r'cirq.Z',"cirq.S",new_codeline)+"# number="+str(number+1)+"\n"
        return codeline
    else:
        raise Exception('No Z gate for S transformation')

def x_to_hssh(codeline:str,number:int):
    if re.search('cirq.X',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline = re.sub(r'cirq.X',"cirq.H",new_codeline)+"# number="+str(number)+"\n"+\
                   re.sub(r'cirq.X',"cirq.S",new_codeline)+"# number="+str(number+1)+"\n"+ \
                   re.sub(r'cirq.X', "cirq.S", new_codeline)+"# number="+str(number+2)+"\n" + \
                   re.sub(r'cirq.X', "cirq.H", new_codeline) + "# number=" + str(number + 3) + "\n"
        return codeline
    else:
        raise Exception('No X gate for HSSH transformation')