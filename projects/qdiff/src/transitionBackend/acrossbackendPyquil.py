#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:19 PM
# @Author  : anonymous
# @File    : acrossbackendPyquil.py

import transitionBackend.Pyquilbackend as Pb
import re
import random
pragma_pattern = ['NAIVE','PARTIAL','GREEDY']

def generate(address: str, name: str, iteration: int):
    simup = re.compile("startPyquil")


    if simup.search(name):
        return Pb.simulator_to_pragma(address,iteration), Pb.simulator_to_state_vector(address,iteration)
    else:
        print("Error: backend transition failed. We do not start from simulator")

