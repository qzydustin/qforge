import sys
import subprocess

valid_compiler: list = []

MLIR_filename = "test.mlir"
PASS_PHASES = [
    "esi-connect-services",
    "lower-hwarith-to-hw",
    "lower-scf-to-calyx",
    "msft-lower-constructs",
    "msft-lower-instances",
    #"esi-emit-collateral{schema-file=schema.capnp}",
    "hw.module(lower-seq-hlmem)",
    "lower-esi-to-physical",
    "lower-esi-ports",
    "lower-esi-to-hw",
    "convert-fsm-to-sv",
    "lower-seq-to-sv",
    "canonicalize",
    "cse",
    "lower-calyx-to-hw",
    "hw.module(prettify-verilog), hw.module(hw-cleanup)",
    "msft-export-tcl{tcl-file=target.tcl}"
]


def execute_compiler(compiler_opt, compiler, mlir_name, initial_error=None) -> (bool, str):
    global valid_compiler
    try:
        output = subprocess.check_output([compiler_opt,
                                          "-pass-pipeline=builtin.module(" + ','.join(compiler) + ")",
                                          mlir_name], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as error:
        lines = str(error.output).split("\n")
        for line in lines:
            if ("Assertion" in line) and ("failed" in line):
                lines[0] = line
                break
        if ("tmp/tmp" in lines[0]) and ("error" in lines[0]):
            last_colon_position = lines[0].rfind(':')
            lines[0] = lines[0][last_colon_position:]
        if lines[0] == initial_error:
            valid_compiler.append(compiler)
            return True, lines[0]
        elif initial_error is None:
            valid_compiler.append(compiler)
            return True, lines[0]
        else:
            return False, lines[0]
    if initial_error == "True":
        valid_compiler.append(compiler)
        return True, "True"
    elif initial_error is not None:
        return False, "True"
    valid_compiler.append(compiler)
    return True, "True"


def find_dependency(compiler_opt, passes, mlir_name):
    initial_flag, initial_error = execute_compiler(compiler_opt, passes, mlir_name)
    dependency: dict = {}
    flag = initial_flag
    while (len(passes) > 1) and flag:
        passes = passes[:-1]
        flag, new_error = execute_compiler(compiler_opt, passes, mlir_name, initial_error)
    while len(passes) > 1:
        n = len(passes) - 1
        Pn_dependency = set()
        for i in range(n - 1, -1, -1):
            # Construct Ci
            Ci = passes[:i]

            # Add current dependencies to Ci to make Ci'
            Ci_prime = Ci + list(Pn_dependency) + [passes[-1]]

            # Execute Ci'
            flag, new_error = execute_compiler(compiler_opt, Ci_prime, mlir_name, initial_error)
            if flag is False:
                Pn_dependency.add(passes[i])
        dependency[passes[-1]] = Pn_dependency
        passes = passes[:-1]
    return dependency, initial_error, valid_compiler


if __name__ == '__main__':
    #JW: Still not right, new circt need "error: expected pass pipeline to be wrapped with the anchor operation type, e.g. 'builtin.module(...)'"
    dependency, initial_error, valid_compiler = find_dependency(PASS_PHASES, MLIR_filename)
    print(valid_compiler)
    print(len(valid_compiler))
    print(dependency)
    print(initial_error)