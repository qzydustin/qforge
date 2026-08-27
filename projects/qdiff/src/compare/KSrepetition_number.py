#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/19/21 11:14 AM
# @File    : repetition_number.py

import random

if __name__ == '__main__':


    for auto in range(16):

        ave = 0.0
        experiment = 200
        repetition = 1000 * (auto + 1)


        for j in range(experiment):
            n = 2
            answer = [0]*n

            for i in range(repetition):
                k = random.randint(0,n-1)
                answer[k] = answer[k] + 1

            max = 0.0
            for i in range(n):
                if abs(answer[i]-repetition/n)>max:
                    max = abs(answer[i]-repetition/n)

            ave = ave+max/experiment
            ks = ave/repetition

        print("repetition",repetition)
        print("KS:",ks)