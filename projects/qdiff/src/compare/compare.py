#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/3/20 10:33 AM
# @File    : __init__.py

import re,os
import numpy as np
from math import log2
from compare.threshold_repetition import KSRepetition
from compare.threshold_repetition import EntropyRepetition

class Compare:

    threshold = 0
    address = ''
    qubit_number = 0

    def __init__(self, address, threshold, qubit_number):
        self.address = address
        self.threshold = threshold
        self.qubit_number = qubit_number

    def trans_str(self, number: int) -> str:

        results = bin(number)
        results = results[2:len(results)]

        return results.zfill(self.qubit_number)

    def score(self, r1:[], r2:[]) -> float:
        return 0


    def compare(self):
        path = self.address
        qubit_number = self.qubit_number
        threshold = self.threshold
        print("qubit_number:", qubit_number)
        data = []
        name = []
        right_file = re.compile("start")
        files = os.listdir(path)
        for file in files:
            if (not os.path.isdir(file)) & (right_file.search(file) is not None):
                data.append(self.read_results(self.address+"/"+file))
                name.append(file)

        candidates = []  # save right answer candidates
        answer = -1

        for results in data:

            flag = -1
            for i in range(0, len(candidates)):
                if self.score(candidates[i] / (candidates[i].sum()),
                            np.asarray(results) / (np.asarray(results).sum())) < threshold:
                    flag = i
                    candidates[i] = candidates[i] + np.asarray(results)
                    if candidates[i].sum() > candidates[answer].sum():
                        answer = i
                    break

            if flag == -1:
                candidates.append(np.asarray(results))
                if answer == -1:
                    answer = 0

        wrong_out = []  # wrong_out -> the output that is more than threshold could bare
        max_diff = 0  # max k_S score
        print("Right answer:", candidates[answer] / candidates[answer].sum() * 1024)
        max_diff_name = ''

        for i in range(0, len(data)):
            k = self.score(np.asarray(data[i]) / np.asarray(data[i]).sum(), candidates[answer] / candidates[answer].sum())
            if k > max_diff:
                max_diff = k
                max_diff_name = name[i]
            if k > threshold:
                print(k)
                print(name[i] + ":" + str(data[i]))
                wrong_out.append(name[i])

        return wrong_out, max_diff, max_diff_name

    def trans(self, data: str, flag1: int):  # flag1: to check if the order is upside down
        result = re.split(',|}', data)
        final_data = []


        for i in range(0, pow(2, self.qubit_number)):
            if flag1 == 0:
                pattern = re.compile(self.trans_str(i) + "':")
            else:
                pattern = re.compile(''.join(reversed(self.trans_str(i))) + "':")
            flag = 0
            for results in result:
                s = re.search(pattern, results)
                if s is not None:
                    final_data.append(float(results[s.span()[1]:]))
                    flag = 1
            if flag == 0:
                final_data.append(0)

        return final_data

    def read_results(self,path:str):

        filename = path
        pattern_qiskit = re.compile("Qiskit")
        pattern_pyquilc = re.compile("Pyquil_Class")
        flag1 = 0
        with open(filename, 'r') as f:
            print("Now read:" + filename)
            if (re.search(pattern_pyquilc, filename) is not None) or (re.search(pattern_qiskit, filename) is not None):
                flag1 = 1
            line = f.readline()

            end_file = line
            while end_file:
                end_file = f.readline()
                line = line + end_file
            data = self.trans(line, flag1)

        return data




class KSScore(Compare):

    def __init__(self, address, threshold, qubit_number):
        Compare.__init__(self,address,threshold,qubit_number)

    def score(self, r1:[], r2:[]):
        r = r1 - r2
        max_ks = max(max(r), 0)
        min_ks = min(min(r), 0)
        return (abs(max_ks) + abs(min_ks)) / r1.sum()



class CrossEntropy(Compare):

    def __init__(self, address, threshold, qubit_number):
        Compare.__init__(self,address,threshold,qubit_number)

    def score(self, r_true: [], r_false: []):

        h = 0.0
        for i in range(0, len(r_true)):
            if r_false[i] != 0:
                h = -r_true[i] * log2(r_false[i]) + h
            else:
                h = -r_true[i] * log2(1 / 1024) + h
        return h

    def compare(self):
        print("qubit_number:", self.qubit_number)
        data = []
        name = []
        right_file = re.compile("start")
        right_answer_file = re.compile("Cirq_Class")
        files = os.listdir(self.address)
        candidates = []  # save right answer candidates, first candidate will be matrix results

        for file in files:
            if (not os.path.isdir(file)) & (right_file.search(file) is not None):
                data.append(self.read_results(self.address+"/"+file))
                name.append(file)
            if right_answer_file.search(file) is not None:
                candidates.append(np.asarray(self.read_results(self.address+ "/" + file)))

        answer = 0

        for results in data:

            flag = -1
            for i in range(0, len(candidates)):
                if self.score(candidates[i] / (candidates[i].sum()),
                                 np.asarray(results) / (np.asarray(results).sum())) < self.threshold:
                    flag = i
                    candidates[i] = candidates[i] + np.asarray(results)
                    if candidates[i].sum() > candidates[answer].sum():
                        answer = i
                    break

            if flag == -1:
                candidates.append(np.asarray(results))

        wrong_out = []  # wrong_out -> the output that is more than threshold could bare
        max_diff = 0
        print("Right answer:", candidates[answer] / candidates[answer].sum() * 1024)
        max_diff_name = ''

        for i in range(0, len(data)):
            k = self.score(np.asarray(data[i]) / np.asarray(data[i]).sum(),
                              candidates[answer] / candidates[answer].sum())
            if k > max_diff:
                max_diff = k
                max_diff_name = name[i]
            if k > self.threshold:
                print(k)
                print(name[i] + ":" + str(data[i]))
                wrong_out.append(name[i])

        return wrong_out, max_diff, max_diff_name


