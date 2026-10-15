#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/4/20 9:55 AM
# @Author  : anonymous
# @File    : Mutation_shadow.py
# Only support reversion for self-reverse gate

import re
rever_self = ["H","X","Z","Y","CNOT","SWAP","CZ"]

def reverse_gate(Quantumgate:str):
    if Quantumgate in rever_self:
        return Quantumgate

def generate_reverse(address_in:str, address_out:str):

    end_find = re.compile("# circuit end")
    writefile_address = "../data/reverse/" + address_out[21:-3] + ".csv"
    writefile_find = re.compile("../data/" + address_in[13:-3] + ".csv")

    readfile = open(address_in)
    writefile = open(address_out, "w")
    line = readfile.readline()

    is_operation = re.compile("# number=")

    stack=[]

    while line:

        if writefile_find.search(line) is not None:
            writefile.write(re.sub(writefile_find,writefile_address,line))
            line = readfile.readline()
            continue

        if end_find.search(line) is not None:
            stack.reverse()
            for write_line in stack:
                writefile.write(write_line)

        writefile.write(line)

        if is_operation.search(line) is not None:
            stack.append(line)

        line = readfile.readline()

    readfile.close()
    writefile.close()
    return address_out



if __name__ == '__main__':
    generate_reverse("../benchmark/startCirq_Class10.py","../benchmark/reverse/startCirq_class10.py")