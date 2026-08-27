#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/25/21 11:16 AM
# @Author  : anonymous
# @File    : pairComparison.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/20 4:58 PM
# @Author  : anonymous
# @File    : compareResults.py


import numpy as np
import os
import re
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import heapq

def ks_score(r1, r2):
    r = r1-r2
    max_ks = max(max(r), 0)
    min_ks = min(min(r), 0)
    return (abs(max_ks)+abs(min_ks))/r1.sum()

def trans_str(qubit_number:int, number:int)->str:

    results = bin(number)
    results = results[2:len(results)]

    return results.zfill(qubit_number)

def trans(data:str,qubit_number:int,flag1:int): #flag1: to check if the order is upside down
    result = re.split(',|}',data)
    final_data = []

    for i in range(0,pow(2,qubit_number)):
        if flag1==0:
            pattern = re.compile(trans_str(qubit_number,i)+"':")
        else:
            pattern = re.compile(''.join(reversed(trans_str(qubit_number,i)))+"':")
        flag = 0
        for results in result:
            s = re.search(pattern,results)
            if s is not None:
                final_data.append(float(results[s.span()[1]:]))
                flag = 1
        if flag==0:
            final_data.append(0)

    return final_data

def read_results(filename: str, qubit_number:int):

    pattern_qiskit = re.compile("Qiskt")
    pattern_pyquilc = re.compile("Pyquil_Class")
    flag1 = 0
    with open(filename, 'r') as f:
        print("Now read:"+filename)
        if (re.search(pattern_pyquilc,filename) is not None) or (re.search(pattern_qiskit,filename) is not None):
            flag1 = 1
        line = f.readline()

        end_file = line
        while end_file:
            end_file=f.readline()
            line = line+end_file
        data = trans(line, qubit_number,flag1)
    return data

def compare(path:str, thershold:float, qubit_number:int):
    print("qubit_number:",qubit_number)
    data = []
    name = []
    right_file = re.compile("startQiskit")
    files = os.listdir(path)
    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            data.append(read_results(path+"/"+file, qubit_number))
            name.append(file)

    candidates = [] # save right answer candidates
    answer = -1

    pair_data = []
    k=3

    for i in range(0, len(data)):
        results1 = data[i]
        for j in range(i, len(data)):
            results2 = data[j]
            pair_data.append(ks_score(np.asarray(results1)/(np.asarray(results1).sum()),np.asarray(results2)/(np.asarray(results2).sum())))

    top_k = heapq.nlargest(k,pair_data)
    print(top_k)
    top_k_value =top_k[-1]

    for i in range(0, len(data)):
        results1 = data[i]
        for j in range(i, len(data)):
            results2 = data[j]
            value = ks_score(np.asarray(results1)/(np.asarray(results1).sum()),np.asarray(results2)/(np.asarray(results2).sum()))
            if value>top_k_value:
                print(name[i]+"vs"+name[j])
                print("K-s:",value)

if __name__ == '__main__':
    ans=0

    for i in range(50,99):
        compare("../data/Qiskit_new1/"+str(i)+"/",0.1,4)
        print("Next round")

