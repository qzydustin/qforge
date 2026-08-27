#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:00 PM
# @File    : acrossbackendCirq.py

import transitionBackend.Cirqbackend as Cb
import re

def generate(address:str, name:str, iteration:int):
    simup = re.compile("startCirq")

    if simup.search(name):
        return Cb.simulator_to_pragma(address, iteration), Cb.simulator_to_state_vector(address, iteration), Cb.simulator_to_noisy(address,iteration)
    else:
        print("Error: backend transition failed. We do not start from simulator")

