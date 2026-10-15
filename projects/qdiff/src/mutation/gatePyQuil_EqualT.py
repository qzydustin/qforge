#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 2:59 PM
# Quantum transformation rules
# @File    : MutatePyQuil_equal.py

#TODO: test transformation

import re

def cnot_to_hczh(codeline:str,number:int):
    if re.search('CNOT', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('CNOT[(](.*)[,]', "H(", new_codeline)+"# number="+str(number)+"\n"+ \
               re.sub('CNOT', "CZ", new_codeline)+"# number="+str(number+1)+"\n"+ \
               re.sub('CNOT[(](.*)[,]',"H(", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No CNOT gate for CZ transformation')

def cz_to_hcnoth(codeline:str,number:str):
    if re.search('CZ',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('CZ[(](.*)[,]', "H(", new_codeline) + "# number=" + str(number) + "\n" + \
               re.sub('CZ', "CNOT", new_codeline) + "# number=" + str(number + 1) + "\n" + \
               re.sub('CZ[(](.*)[,]', "H(", new_codeline) + "# number=" + str(number + 2) + "\n"
    else:
        raise Exception('No CZ gate for CNOT transformation')

def order_change(codeline1:str, codeline2:str):
    return codeline2, codeline1

def swap_to_cnot(codeline:str,number:int):
    if re.search('SWAP', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('SWAP', "CNOT", new_codeline)+"# number="+str(number)+"\n"+ \
               re.sub('SWAP', "CNOT", new_codeline)+"# number="+str(number+1)+"\n"+ \
               re.sub('SWAP',"CNOT", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Swap gate for Swap transformation')

def x_to_cnotxcnot(codeline:str,number:int):
    help_qubit_now = re.compile("X[(]")
    help_qubit = int(codeline[help_qubit_now.search(codeline).span()[1]]) #can not handle 10+ qubits
    if help_qubit==0:
        help_qubit = 1
    else:
        help_qubit = 0
    if re.search('X', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('X[(]', "CNOT("+str(help_qubit)+",", new_codeline)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'X[(]', "CNOT("+str(help_qubit)+",", new_codeline)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No X gate for X transformation')

def z_to_cnotzcnot(codeline:str,number:int):
    help_qubit_now = re.compile("Z[(]")
    help_qubit = int(codeline[help_qubit_now.search(codeline).span()[1]]) #can not handle 10+ qubits
    if help_qubit==0:
        help_qubit = 1
    else:
        help_qubit = 0
    if re.search('Z', codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline1 = re.sub(r'Z', "CNOT", new_codeline)
        return re.sub(r'[)]', ","+str(help_qubit)+")", codeline1,count=1)+"# number="+str(number)+"\n"+\
               new_codeline+"# number="+str(number+1)+"\n"+\
               re.sub(r'[)]', ","+str(help_qubit)+")", codeline1,count=1)+"# number="+str(number+2)+"\n"
    else:
        raise Exception('No Z gate for Z transformation')

def two_X(tab:str,qubit_number:int, number:int):
    return tab+"prog += X("+str(qubit_number)+") # number="+str(number)+"\n"+\
           tab+"prog += X("+str(qubit_number)+") # number="+str(number+1)+"\n"

def two_Y(tab:str, qubit_number:int, number:int):
    return tab+"prog += Y("+str(qubit_number)+") # number="+str(number)+"\n"+\
           tab+"prog += Y("+str(qubit_number)+") # number="+str(number+1)+"\n"

def two_CNOT(tab: str, qubit_number: int, number: int):
    return tab+"prog += CNOT("+str(qubit_number)+",0) # number="+str(number)+"\n"+\
           tab+"prog += CNOT("+str(qubit_number)+",0) # number="+str(number+1)+"\n"

def two_SWAP(tab:str, qubit_number:int, number:int):
    return tab + "prog += SWAP(" + str(qubit_number) + ",0) # number=" + str(number) + "\n" + \
           tab + "prog += SWAP(" + str(qubit_number) + ",0) # number=" + str(number + 1) + "\n"

def s_to_t(codeline:str,number:int):
    if re.search('S',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        return re.sub('S', "T", new_codeline) + "# number=" + str(number) + "\n" + \
               re.sub('S', "T", new_codeline) + "# number=" + str(number + 1) + "\n"
    else:
        raise Exception('No S gate for T transformation')

def z_to_s(codeline:str,number:int):
    if re.search('Z',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline = re.sub(r'Z',"S",new_codeline)+"# number="+str(number)+"\n"+\
                   re.sub(r'Z',"S",new_codeline)+"# number="+str(number+1)+"\n"
        return codeline
    else:
        raise Exception('No Z gate for S transformation')

def x_to_hssh(codeline:str,number:int):
    if re.search('X',codeline) is not None:
        new_codeline = re.sub("# number=(.*)[\n]", "", codeline)
        codeline = re.sub(r'X',"H",new_codeline)+"# number="+str(number)+"\n"+\
                   re.sub(r'X',"S",new_codeline)+"# number="+str(number+1)+"\n"+ \
                   re.sub(r'X', "S", new_codeline)+"# number="+str(number+2)+"\n" + \
                   re.sub(r'X', "H", new_codeline) + "# number=" + str(number + 3) + "\n"
        return codeline
    else:
        raise Exception('No X gate for HSSH transformation')