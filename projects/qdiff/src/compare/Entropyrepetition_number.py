#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/19/21 11:14 AM
# @File    : repetition_number.py

import random
from math import log2

if __name__ == '__main__':


    for auto in range(16):

        ave = 0.0
        experiment = 200
        repetition = 200 * (auto + 1)


        for j in range(experiment):
            n = 4
            answer = [0]*n

            for i in range(repetition):
                k = random.randint(0,n-1)
                answer[k] = answer[k] + 1

            h = 0.0
            for i in range(n):
                h = -1/n * log2(answer[i]/repetition) + h

            ave = ave+h/experiment
            ks = ave/repetition*1000

        print("repetition",repetition)
        print("entropy:",ave)