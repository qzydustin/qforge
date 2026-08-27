import copy, multiprocessing, re, subprocess, sys, time, random
from itertools import combinations
from typing import List
from mlir.dialects import *
from mlir.ir import Context, InsertionPoint, Location, Module, Operation, Block, TypeAttr, FunctionType
import mlir
from dependency import find_dependency as quick_find
import random

import inspect

Integer_type_pattern = r'\s*i\d+|index'
Float_type_pattern = r'\s*f\d+'
Integer_array_type_pattern = r'\s*vector<\d+xi\d+>'
Float_array_type_pattern = r'\s*vector<\d+xf\d+>'
Bool_array_type_pattern = r'\s*vector<\d+xi1>'
Bool_type_pattern = r'\s*i1'
Integer_constant = "42"
Float_constant = "42.000000"
Bool_constant = "True"
Integer_array_constant = "dense<42>"
Float_array_constant = "dense<42.00000e+00>"
Bool_array_constant = "dense<True>"
Patterns = [(Float_array_type_pattern, Float_array_constant), (Integer_array_type_pattern, Integer_array_constant),
            (Bool_array_type_pattern, Bool_array_constant), (Float_type_pattern, Float_constant),
            (Integer_type_pattern, Integer_constant), (Bool_type_pattern, Bool_constant)]


def operator_list(code: str) -> set:
    operator_pattern = r'%\d+'
    matches = re.findall(operator_pattern, code)
    return set(matches)


def cut_entry(code_lines):
    candidate_code_constant = []
    candidate_code_vf = []
    for code_line in code_lines:
        pre_count = code_line.count('%')
        if pre_count > 1:
            parts = code_line.split("=", 1)
            if parts:
                left_operator = parts[0].strip()
            else:
                continue
            print("merge point find for:", left_operator)
            constant_changed_code = refactor_fixed_code(code_lines, left_operator, "constant replace")
            vf_changed_code = refactor_fixed_code(code_lines, left_operator, "virtual function")
            candidate_code_constant.append(constant_changed_code.strip().split('\n'))
            candidate_code_vf.append(vf_changed_code.strip().split('\n'))
    return candidate_code_constant + candidate_code_vf


def replace_constant(operator: str, target_code_line: str) -> str:
    print("replacement happen for", target_code_line)
    if not (operator in target_code_line):
        raise "Wrong"
    try:
        last_colon_position = target_code_line.rfind(':')
        op_type = target_code_line[(last_colon_position + 1):]
    except:
        raise "Wrong, no ':'"
    if " to " in op_type:
        op_type = op_type.split(" to")[-1]
    if "index." in target_code_line:
        op_type = "index"

    for pattern, constant in Patterns:
        if re.match(pattern, op_type):
            return operator + "= arith.constant " + constant + ":" + op_type
    return target_code_line


def insert_virtual_function_def(operator: str, target_code_line: str) -> (str, str):
    if not (operator in target_code_line):
        raise "Wrong"
    try:
        last_colon_position = target_code_line.rfind(':')
        op_type = target_code_line[(last_colon_position + 1):]
    except:
        raise "Wrong, no ':'"
    if " to " in op_type:
        op_type = op_type.split(" to")[-1]
    if "index." in target_code_line:
        op_type = "index"

    function_name = "@malloc" + str(random.randint(0, 100))
    virtual_func_line = "llvm.func " + function_name + "(" + op_type + ")" + "->" + op_type
    return virtual_func_line, function_name


def insert_virtual_function_call(operator: str, target_code_line: str, function_name: str) -> str:
    # virtual_func_line, function_name = insert_virtual_function_def(operator, target_code_line)
    if not (operator in target_code_line):
        raise "Wrong"
    try:
        last_colon_position = target_code_line.rfind(':')
        op_type = target_code_line[(last_colon_position + 1):]
    except:
        raise "Wrong, no ':'"
    if " to " in op_type:
        op_type = op_type.split(" to")[-1]
    if "index." in target_code_line:
        op_type = "index"

    new_op = "%" + str(random.randint(1000, 2000))
    virtual_call_code_line = new_op + "=llvm.call " + function_name + "(" + operator + "):(" + op_type + ")" + "->" + op_type
    return virtual_call_code_line


def refactor_fixed_code(code_lines, operator: str, mutation_type: str) -> str:
    changed_code = ""
    if mutation_type == "constant replace":
        for i in range(len(code_lines)):
            code_line = code_lines[i]
            if ((operator + " =") in code_line) or (operator + "=" in code_line):
                changed_code = changed_code + "\n" + replace_constant(operator, code_line)
            else:
                changed_code = changed_code + "\n" + code_line
        return changed_code
    elif mutation_type == "virtual function":
        for i in range(len(code_lines)):
            code_line = code_lines[i]
            changed_code = changed_code + "\n" + code_line
            if ((operator + " =") in code_line) or (operator + "=" in code_line):
                virtual_function = insert_virtual_function_def(operator, code_line)
                changed_code = virtual_function[0] + changed_code
                changed_code = changed_code + "\n" + insert_virtual_function_call(operator, code_line,
                                                                                  virtual_function[1])
        return changed_code
    else:
        raise "Transformation not supported"


if __name__ == '__main__':
    original_ir_code_file = sys.argv[1]
    f = open(original_ir_code_file, "r")
    original_ir_code = f.read()
    print(refactor_fixed_code(original_ir_code, "%245", "virtual function"))
