#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/7/21 8:22 AM
# @File    : crossEntropy.py

from math import log2
import numpy as np
import re
import os

def entropy_score(r_true:[],r_false:[]):

    h = 0.0
    for i in range(0,len(r_true)):
        if r_false[i]!=0:
            h = -r_true[i] * log2(r_false[i])+h
        else:
            h = -r_true[i] * log2(1/1000) + h

    return h

def read_results(filename: str, qubit_number:int):

    pattern_qiskit = re.compile("Qiskit")
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

def trans_str(qubit_number:int, number:int)->str:

    results = bin(number)
    results = results[2:len(results)]

    return results.zfill(qubit_number)


def compare(path:str, thershold:float, qubit_number:int):
    print("qubit_number:",qubit_number)
    data = []
    name = []
    right_file = re.compile("start")
    right_answer_file = re.compile("Qiskit_Class")
    files = os.listdir(path)
    candidates = []  # save right answer candidates, first candidate will be matrix results


    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            data.append(read_results(path+"/"+file, qubit_number))
            name.append(file)
        if right_answer_file.search(file) is not None:
            candidates.append(np.asarray(read_results(path+"/"+file, qubit_number)))

    answer = 1


    """
    for results in data:

        flag = -1
        for i in range(0,len(candidates)):
            if entropy_score(candidates[i]/(candidates[i].sum()),np.asarray(results)/(np.asarray(results).sum()))<thershold:
                flag = i
                candidates[i] = candidates[i] + np.asarray(results)/(np.asarray(results).sum())
                if candidates[i].sum() > candidates[answer].sum():
                    answer = i
                break

        if flag == -1:
            candidates.append(candidates.append(np.asarray(results)/(np.asarray(results).sum())))
    """

    wrong_out = []      # wrong_out -> the output that is more than threshold could bare
    max_diff = 0
    print("Right answer:",candidates[answer]/candidates[answer].sum()*1024)
    max_diff_name = ''
    print(entropy_score(candidates[answer]/candidates[answer].sum(),candidates[answer]/candidates[answer].sum()))
    for i in range(0, len(data)):
        k = entropy_score(candidates[answer]/candidates[answer].sum(),np.asarray(data[i])/np.asarray(data[i]).sum())-\
            entropy_score(candidates[answer]/candidates[answer].sum(),candidates[answer]/candidates[answer].sum())
        if k > max_diff:
            max_diff = k
            max_diff_name = name[i]
        if k > thershold:
            print(k)
            print("Wrong"+name[i]+":"+str(data[i]))
            wrong_out.append(name[i])


    return wrong_out, max_diff, max_diff_name

if __name__ == '__main__':
    ans=0
    for i in range(0,10):
        a1,average,a2 = compare("../data/Qiskit_new1/"+str(i)+"/",0.03,4)
        ans+=average
        print(compare("../data/Qiskit_new1/"+str(i)+"/",0.03,4))