#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/29/20 3:19 PM
# @Author  : anonymous
# @File    : acrossbackendQiskit.py

import transitionBackend.Qiskitbackend as Qb
import re


def generate(address: str, name: str, iteration: int):
    simup = re.compile("startQiskit")


    if simup.search(name):
        return Qb.simulator_to_noisy(address,iteration), Qb.simulator_to_state_vector(address,iteration), \
               Qb.simulator_to_qc(address,iteration)
    else:
        print("Error: backend transition failed. We do not start from simulator")