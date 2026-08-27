#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2/7/21 8:02 PM
# @File    : serious_gate_transback.py

class TransformBack:

    gate_number = 0
    gate_sequence = []
    out_gate = []

    def __init__(self, gate_number:int, gate_sequence:[], out_gate:[]):
        self.gate_number = gate_number
        self.gate_sequence = gate_sequence
        self.out_gate = out_gate

    def check(self, input_gate_sequence:[],) -> bool:
        if input_gate_sequence==self.gate_sequence:
            return True
        else:
            return False