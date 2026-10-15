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
    right_file = re.compile("startQiskit_QC") # only consider Qiskit noisy
    #right_file = re.compile("startQiskit")
    #right_file = re.compile("start)
    files = os.listdir(path)
    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            data.append(read_results(path+"/"+file, qubit_number))
            name.append(file)

    candidates = [] # save right answer candidates
    answer = -1



    for results in data:

        flag = -1
        for i in range(0,len(candidates)):
            if ks_score(candidates[i]/(candidates[i].sum()),np.asarray(results)/(np.asarray(results).sum()))<thershold:
                flag = i
                candidates[i] = candidates[i] + np.asarray(results)/(np.asarray(results).sum())
                if candidates[i].sum() > candidates[answer].sum():
                    answer = i
                break

        if flag == -1:
            candidates.append(np.asarray(results)/(np.asarray(results).sum()))
            if answer == -1:
                answer = 0

    wrong_out = []      # wrong_out -> the output that is more than threshold could bare
    max_diff = 0        # max k_S score
    print("Right answer:",candidates[answer]/candidates[answer].sum()*1024)



    max_diff_name = ''

    for i in range(0, len(data)):
        k = ks_score(np.asarray(data[i])/np.asarray(data[i]).sum(),candidates[answer]/candidates[answer].sum())
        if k > max_diff:
            max_diff = k
            max_diff_name = name[i]
        if k > thershold:
            print(k)
            print(name[i]+":"+str(data[i])+":"+str(k))
            wrong_out.append(name[i])


    return wrong_out, max_diff, max_diff_name

if __name__ == '__main__':
    ans=0


    for i in range(12,99):
        #a1, average, a2 = compare("../data/Qiskit_new2/"+str(i)+"/",0.1,4)
        print(compare("../data/p4VQE/R3/Wrong"+str(i)+"/",0.4,5))
        os.system('mv ../data/p4VQE/R3/Wrong'+str(i)+' ../data/p4VQE/R3/'+str(i))
