#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/26/21 3:59 PM
# @File    : threshold-repetition.py

import math

class ThresholdRepetition:

    threshold : float
    max_p : float
    qubit_state_number : int

    def __init__(self, threshold, max_p, qubit_state_number):

        self.threshold = threshold
        self.max_p = max_p
        self.qubit_state_number = qubit_state_number

    def repetition(self) -> int:

        return 0


class KSRepetition(ThresholdRepetition):

    def repetition(self):

        return 14 * round(math.sqrt(self.qubit_state_number) / (self.threshold * self.threshold))

class EntropyRepetition(ThresholdRepetition):

    def repetition(self):

        return 20 * round(self.max_p * math.sqrt(self.max_p * self.qubit_state_number) / (self.threshold * self.threshold))