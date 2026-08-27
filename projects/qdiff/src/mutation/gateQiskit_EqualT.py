#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 3:12 PM
# Quantum transformation rules
# @File    : MutateQiskit_equal.py

#TODO: test transformation


import re

def cnot_to_hczh(codeline:str,number:int):
    if re.search('prog.cx', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('cx[(](.*)[,]', "h(", new_codeline)+"# number="+str(number)+"\n"+\
               re.sub('cx', "cz", new_codeline)+"# number="+str(number+1)+"\n"+\
               re.sub('cx[(](.*)[,]',"h(", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No CNOT gate for CZ transformation')

def cz_to_hcnoth(codeline:str,number:int):
    if re.search('prog.cz', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('cz[(](.*)[,]', "h(", new_codeline)+"# number="+str(number)+"\n"+\
               re.sub('cz', "cx", new_codeline)+"# number="+str(number+1)+"\n"+\
               re.sub('cz[(](.*)[,]',"h(", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No CZ gate for CNOT transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def cx_to_cnot(codeline:str,number:int):
    if re.search('prog.cx',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('cx','cnot',new_codeline)+"# number="+str(number)+"\n"
    else:
        raise Exception('No Cx gate for Cnot transformation')

def swap_to_cnot(codeline:str,number:int):
    if re.search('prog.swap', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('swap', "cx", new_codeline)+"# number="+str(number)+"\n"+\
               re.sub('swap', "cx", new_codeline)+"# number="+str(number+1)+"\n"+\
               re.sub('swap',"cx", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str,number:int):
    help_qubit_now = re.compile("prog.x[(]input_qubit[[]")
    help_qubit = int(codeline[help_qubit_now.search(codeline).span()[1]]) #can not handle 10+ qubits
    if help_qubit==0:
        help_qubit = 1
    else:
        help_qubit = 0
    if re.search('prog.x', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('x[(]', "cx(input_qubit["+str(help_qubit)+"],", new_codeline)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'x[(]', "cx(input_qubit["+str(help_qubit)+"],", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str,number:int):
    help_qubit_now = re.compile("prog.z[(]input_qubit[[]")
    help_qubit = int(codeline[help_qubit_now.search(codeline).span()[1]]) #can not handle 10+ qubits
    if help_qubit==0:
        help_qubit = 1
    else:
        help_qubit = 0
    if re.search('prog.z', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline1 = re.sub(r'z', "cx", new_codeline)
        return re.sub(r'[)]', ",input_qubit["+str(help_qubit)+"])", codeline1,count=1)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'[)]', ",input_qubit["+str(help_qubit)+"])", codeline1,count=1)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Z gate for Z transformation')

def two_X(tab:str, qubit_number:int, number:int):
    return tab+"prog.x(input_qubit["+str(qubit_number)+"]) # number="+str(number)+"\n"+\
           tab+"prog.x(input_qubit["+str(qubit_number)+"]) # number="+str(number+1)+"\n"

def two_Y(tab:str, qubit_number:int, number:int):
    return tab + "prog.y(input_qubit[" + str(qubit_number) + "]) # number=" + str(number ) + "\n" + \
           tab + "prog.y(input_qubit[" + str(qubit_number) + "]) # number=" + str(number + 1) + "\n"

def two_CNOT(tab:str, qubit_number:int, number:int):
    return tab+ "prog.cx(input_qubit[1],input_qubit[0]) # number=" + str(number) +"\n" +\
           tab+ "prog.cx(input_qubit[1],input_qubit[0]) # number=" + str(number+1) +"\n" #should be input_qubit[str(qubit_number)]

def two_SWAP(tab:str, qubit_number:int, number:int):
    return tab + "prog.swap(input_qubit[" + str(qubit_number) + "],input_qubit[0]) # number=" + str(number) + "\n" + \
           tab + "prog.swap(input_qubit[" + str(qubit_number) + "],input_qubit[0]) # number=" + str(number + 1) + "\n"

def s_to_t(codeline:str,number:int):
    if re.search('prog.s',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline = re.sub(r's',"t",new_codeline)+"# number="+str(number)+"\n"+\
                   re.sub(r's',"t",new_codeline)+"# number="+str(number+1)+"\n"
        return codeline
    else:
        raise Exception('No S gate for T transformation')

def z_to_s(codeline:str,number:int):
    if re.search('prog.z',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline = re.sub(r'z',"s",new_codeline)+"# number="+str(number)+"\n"+\
                   re.sub(r'z',"s",new_codeline)+"# number="+str(number+1)+"\n"
        return codeline
    else:
        raise Exception('No Z gate for S transformation')

def x_to_hssh(codeline:str,number:int):
    if re.search('prog.x',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline = re.sub(r'x',"h",new_codeline)+"# number="+str(number)+"\n"+\
                   re.sub(r'x',"s",new_codeline)+"# number="+str(number+1)+"\n"+ \
                   re.sub(r'x', "s", new_codeline)+"# number="+str(number+2)+"\n" + \
                   re.sub(r'x', "h", new_codeline) + "# number=" + str(number + 3) + "\n"
        return codeline
    else:
        raise Exception('No X gate for HSSH transformation')
