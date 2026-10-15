import copy, multiprocessing, re, subprocess, sys, time, random
from itertools import combinations
from typing import List

from dependency import find_dependency as quick_find

import cut

output_log_file = "output.log"

exe_round = 1
compiler_variants = []


def unique_ordered_elements(elements):
    seen = set()
    unique_elements = []
    for element in elements:
        if element[0] == "@":
            element = element[1:]
        if element not in seen:
            seen.add(element)
            unique_elements.append(element)
    return unique_elements


def find_subsets(input_list):
    output_list = []
    for i in range(1, len(input_list) + 1):
        for combination in combinations(input_list, i):
            output_list.append(",".join(combination))
    return output_list


def get_possible_pass(input_code: str):
    global PASS_PHASES

    pattern = re.compile(r'([^-,\s]+)(?:-([^-,]+))?(?:-([^-,]+))?')
    new_pass = []
    for passes in PASS_PHASES:
        if ("cse" in passes) or ("canonicalize" in passes):
            new_pass.append(passes)
            continue

        matches = pattern.findall(passes)
        result = unique_ordered_elements([item for match in matches for item in match if item])
        for item in result:
            if item in input_code:
                new_pass.append(passes)
                break
    PASS_PHASES = new_pass
    print("Possible Pass:")
    print(PASS_PHASES)
    global compiler_variants
    compiler_variants = find_subsets(PASS_PHASES)
    print("Possible Compiler number:")
    print(len(compiler_variants))


# Jiyuan: maybe we can start from 3rd IR. TypeAlias seems related with system.py

def contact_verilog_code(filename_list):
    contact_code = ""
    for filename in filename_list:
        if not ("sv" in filename):
            filename = filename + ".sv"
        with open(filename, "r") as file:
            contact_code = contact_code + file.read()
    return contact_code


# should add with fused location information (set tag in #snapshot-location), no idea why it can't.
# Now the tracing is done from the desired IR level (ex. IR=4)
# TODO Jiyuan: now the fused information is manually added, should add all fused location information before testing
def location_information_parse(input_text_tracing="", IR=4):
    # input_text_tracing = '''
    # .a      (32'h3),    // after_phase_4.mlir:5:12783; after_phase_3.mlir:3:124
    # .b      (32'h0),    // after_phase_4.mlir:4:1243; after_phase_3.mlir:5:123
    # .b      (32'h1),    // after_phase_4.mlir:4:1243; after_phase_3.mlir:5:123
    # '''

    # Split the input text by lines

    lines = input_text_tracing.strip().split("\n")

    original_dict = {}

    for line in lines:
        # Split the line by '//' to separate the key-value part from the location information
        key_value, locations_text = line.split("//")

        # Remove trailing comma and whitespaces from the key-value part
        key_value = key_value.rstrip(", ").strip()

        # Split the locations_text by ', ' to get individual locations
        locations = locations_text.split("; ")

        # Extract the phase number and line number from each location
        parsed_locations = []
        for loc in locations:
            phase_str, line_col_str = loc.split(".mlir:")
            phase_num = int(phase_str.split("_")[-1])  # Extract the phase number after the last '_'
            line_num = int(line_col_str.split(":")[0])
            parsed_locations.append((phase_num, line_num))

        # Add the key-value and parsed_locations to the result_dict
        original_dict[key_value] = parsed_locations

    new_dict = {}

    for key, values in original_dict.items():
        for value in values:
            if value[0] == IR:
                if value in new_dict:
                    new_dict[value].append(key)
                else:
                    new_dict[value] = [key]

    for key, values in original_dict.items():
        for value in values:
            if value[0] != IR:
                for new_key in new_dict:
                    if key in new_dict[new_key]:
                        new_dict[new_key].append(value)

    # print(new_dict)
    # print(original_dict)
    return new_dict


def extract_error_type(output):
    match = re.search(r"\b\w+Error\b", output)
    if match:
        return match.group(0)
    return None


def verilog_execute(code: str) -> (bool, str):
    verilog_filename = unique_ordered_elements(sv_name_pattern.findall(code))
    if len(verilog_filename) == 0:
        # print("no .sv name specified")
        # print("Warning: using name of the module to find generated .sv file. May introduce bugs")
        verilog_filename = unique_ordered_elements(sv_possible_name_pattern.findall(code))
    if len(verilog_filename) == 0:
        # print("no .sv file generated")
        return False, "no .sv file generated"

    try:
        if not (".sv" in verilog_filename[0]):
            verilog_filename[0] = verilog_filename[0] + ".sv"
        s_compilation_command = ["verilator"] + ["-Wno-fatal"] + ["-cc"] + ["--trace"] + verilog_filename + [
            "--exe"] + ["testbench.cpp"] + ["--top-module"] + [verilog_filename[0][:-3]]
        output = subprocess.check_output(s_compilation_command, stderr=subprocess.STDOUT, text=True)
        output = subprocess.check_output(["make", "-j", "-C", "obj_dir/", "-f", "V" + verilog_filename[0][:-3] + ".mk"],
                                         stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as error:
        print("simulator compilation error: " + error.output)
        return False, error.output

    try:
        output = subprocess.check_output(["./obj_dir/V" + verilog_filename[0][:-3]], stderr=subprocess.STDOUT,
                                         text=True)
        with open(output_log_file, "w") as f:
            print("compilation output:" + output)
            f.write(output)
    except subprocess.CalledProcessError as error:
        print("execution error: " + error.output)
        return False, error.output

    try:
        output = subprocess.check_output(["mkdir", str(exe_round) + "/"], stderr=subprocess.STDOUT,
                                         text=True)
        s_compilation_command = ["mv"] + verilog_filename + [str(exe_round) + "/"]
        output = subprocess.check_output(s_compilation_command, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as error:
        print(error)
        return False, "mkdir error"

    return True, "True"


def test_ir_code(code: str, initial_error: str = None, verilog_execution=False) -> (bool, str):
    # Replace this function with your specific test that returns True if the code causes a failure
    # and False otherwise. For example, you could use a subprocess to run an MLIR pass and check
    # the output or return code.

    global compiler_variants
    randomname = random.randint(1, 100000000)
    MLIR_filename = "tmp/tmp" + str(randomname) + ".mlir"
    with open(MLIR_filename, "w") as f:
        f.write(code)
        f.close()
    generated_verilog_code = set()
    valid_compiler_variants = []
    verilog_filename = unique_ordered_elements(sv_name_pattern.findall(code))
    if len(verilog_filename) == 0:
        # print("no .sv name specified")
        # print("Warning: using name of the module to find generated .sv file. May introduce bugs")
        matches = sv_possible_name_pattern.findall(code)
        verilog_filename = unique_ordered_elements(match[0] if match[0] else match[1] for match in matches)
    # if len(verilog_filename) == 0:
    # print("no .sv file generated")

    if initial_error is not None:
        original_error = initial_error  # assign initial error to this round as the flag
    else:
        original_error = "True"

    start_time = time.time()
    # Figure out the dependency graph if it is the first execution
    if exe_round == 1:
        dependency_graph, original_error, compiler_variants = quick_find(execute_compiler, PASS_PHASES,
                                                                         mlir_name=MLIR_filename)
        print("dependency:", dependency_graph)
        print("passed compiler:", compiler_variants)
        print("initial error:", original_error)

    # Run script if provided
    if script is not None:
        try:
            output = subprocess.check_output([script, MLIR_filename], stderr=subprocess.STDOUT, text=True)
            return True, "True"
        except subprocess.CalledProcessError as error:
            return False, error.output[0]

    # If not, use our own oracle

    for compiler in compiler_variants:  # In each round, dynamically figure out the valid compilation pass
        if (exe_round == 1) and (original_error != "True"):  # avoid repetitive execution for round 1
            if (len(valid_compiler_variants) >= 1) and (len(compiler) < len(valid_compiler_variants[0])):  # save
                # the possible shortest faulty compilation to localize fault, since the compilation is not correct
                valid_compiler_variants[0] = copy.deepcopy(compiler)
            elif len(valid_compiler_variants) < 1:
                valid_compiler_variants.append(compiler)
            continue
        try:
            output = subprocess.check_output([execute_compiler,
                                              "-pass-pipeline=builtin.module(" + ','.join(compiler) + ")",
                                              MLIR_filename], stderr=subprocess.STDOUT, text=True)
            with open(output_log_file, "w") as f:
                f.write(output)

            if original_error != "True":
                continue

            number = len(generated_verilog_code)

            try:
                generated_verilog_code.add(contact_verilog_code(verilog_filename))
            except FileNotFoundError:
                new_error_info = "correct .sv not generated!"

            if number < len(generated_verilog_code):
                # if new code is generated and added into the set, then we found a new valid and unique compiler
                valid_compiler_variants.append(compiler)

            if (len(valid_compiler_variants) == 1) and (len(compiler) < len(valid_compiler_variants[0])):
                # save the shortest compilation path
                valid_compiler_variants[0] = copy.deepcopy(compiler)

        except subprocess.CalledProcessError as error:
            new_error_info = error.output
            if original_error in new_error_info:  # if the same compilation bug reproduced
                if (len(valid_compiler_variants) >= 1) and (len(compiler) < len(valid_compiler_variants[0])):  # save
                    # the possible shortest faulty compilation to localize fault, since the compilation is not correct
                    valid_compiler_variants[0] = copy.deepcopy(compiler)
                elif len(valid_compiler_variants) < 1:
                    valid_compiler_variants.append(compiler)

    # If it is the first round, print out the valid compilation path
    if exe_round == 1:
        print("valid and unique compilation path:", len(valid_compiler_variants))
        print("valid and unique compilation path:", valid_compiler_variants)
        compiler_variants = valid_compiler_variants  # Jiyuan: that's one time effort
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        if original_error != "True":
            return True, original_error
    if len(valid_compiler_variants) == 0:  # if no valid compiler found, return no valid compiler error
        return False, "no valid compiler"

    if verilog_execution:
        return verilog_execute(code)

    # TODO: Above code is tested. Need to think about differential testing =>
    #  now the generated .sv files only contains the last successful compilation:
    #  should have all successful and unique compilation. And the code is stored in generated_verilog_code: see line 138
    print("TEST Compiler", valid_compiler_variants)
    return True, original_error


def codeset_execution(code_set: List[str], initial_flag) -> (List[str], bool):
    for subset in code_set:
        subset_code = '\n'.join(subset)
        if test_ir_code(subset_code, initial_flag[1]) == initial_flag:
            print("pass test!")
            return subset_code.strip().split('\n'), True
    return code_set, False


# TODO: mapping undone
def ddmin_ir(code: str) -> str:
    def split_code(code: List[str], n: int) -> List[List[str]]:
        k, m = divmod(len(code), n)
        #print("k:", k)
        return [code[:i] + code[min(i + n, len(code)):] for i in range(len(code))]

    def divide_array(arr, n, flag):
        k, m = divmod(len(arr), n)
        sets = [arr[i * k: min((i + 1) * k, len(arr))] for i in range(n)]
        ans = []
        for element in sets:
            ans.append((element, flag))
        return ans

    def minimize(code: List[str], initial_flag) -> (List[str], bool):
        if len(code) <= 2:  # if codeline is too small, return False
            return code, False

        n = len(code) - 1
        while len(code) >= n > 0:
            code_sets = divide_array(split_code(code, n), para, initial_flag)
            with multiprocessing.Pool(processes=min(len(code_sets), para)) as pool:
                #print("now at deletion level:", n)
                results = pool.starmap(codeset_execution, iterable=code_sets)
            n = n - 1

            for result in results:
                if result[1]:  # if codeline is too small, return False
                    #print(result[0])
                    return result[0], True
        return code, False

    code_lines = code.strip().split('\n')
    minimized_code_lines = code_lines
    code_dictionary = [(code_lines[i], i) for i in range(len(code_lines))]
    minimized_map = [i for i in range(len(code_lines))]
    initial_flag = test_ir_code(code)
    print("initial flag:", initial_flag)
    global exe_round
    symptom_keep_flag = True
    exe_round = exe_round + 1
    while symptom_keep_flag:
        part_result, symptom_keep_flag = minimize(minimized_code_lines, initial_flag=initial_flag)
        if len(part_result) < len(minimized_code_lines):
            minimized_code_lines = copy.deepcopy(part_result)
        exe_round = exe_round + 1
        if not symptom_keep_flag:
            code_size = len(minimized_code_lines)
            print("Fixed point reached. Try to cut. Now the length is:", code_size)
            code_candidates = cut.cut_entry(minimized_code_lines)
            for i in range(len(code_candidates)):
                code_candidate = code_candidates[len(code_candidates)-i-1]
                part_result, symptom_keep_flag = minimize(code_candidate, initial_flag=initial_flag)
                if len(part_result) < len(minimized_code_lines):
                    minimized_code_lines = copy.deepcopy(part_result)
                    break
            print("Cut. The code size is: ", len(minimized_code_lines))
            symptom_keep_flag = True
            if len(minimized_code_lines) >= code_size:
                print("OK...Seems cut also cannot solve the problem.")
                symptom_keep_flag = False

    return '\n'.join(minimized_code_lines)


# TODO: UnTested

if __name__ == '__main__':
    # Example usage:
    original_ir_code_file = sys.argv[1]
    execute_compiler = sys.argv[2]
    Pass_file = sys.argv[3]
    f = open(original_ir_code_file, "r")
    original_ir_code = f.read()
    f = open(Pass_file, "r")
    PASS_PHASES = f.read().strip().split('\n')
    para = int(sys.argv[4])
    try:
        script = sys.argv[5]
    except IndexError:
        script = None

    #     original_ir_code = """
    # // <python code>
    # module {
    #   msft.module @PolynomialSystem {} () -> (y: i32) attributes {childAppIDBases = ["poly"], fileName = "PolynomialSystem.sv"} {
    #     %c23_i32 = hw.constant 23 : i32
    #     %example.y = msft.instance @example @PolyComputeForCoeff__62__42__6_(%c23_i32)  {msft.appid = #msft.appid<"poly"[0]>} : (i32) -> i32
    #     %example2.y = msft.instance @example2 @PolyComputeForCoeff__62__42__6_(%example.y)  : (i32) -> i32
    #     %example2_1.y = msft.instance @example2_1 @PolyComputeForCoeff__1__2__3__4__5_(%example.y)  : (i32) -> i32
    #     %c23_i32_0 = hw.constant 23 : i32
    #     %b = hw.constant 0 : i32
    #     %0 = comb.divs %example.y, %b : i32
    #     msft.output %0 : i32
    #   }
    #   msft.module @PolyComputeForCoeff__62__42__6_ {coefficients = {coeff = [62, 42, 6]}} (%x: i32) -> (y: i32) attributes {fileName = "PolynomialCompute.sv"} {
    #     %c62_i32 = hw.constant 62 : i32
    #     %c42_i32 = hw.constant 42 : i32
    #     %0 = comb.mul %c42_i32, %x : i32
    #     %1 = comb.add %c62_i32, %0 : i32
    #     %c6_i32 = hw.constant 6 : i32
    #     %2 = comb.mul %x, %x : i32
    #     %3 = comb.mul %c6_i32, %2 : i32
    #     %4 = comb.add %1, %3 : i32
    #     msft.output %4 : i32
    #   }
    #   msft.module @PolyComputeForCoeff__1__2__3__4__5_ {coefficients = {coeff = [1, 2, 3, 4, 5]}} (%x: i32) -> (y: i32) attributes {fileName = "PolynomialCompute.sv"} {
    #     %c1_i32 = hw.constant 1 : i32
    #     %c2_i32 = hw.constant 2 : i32
    #     %0 = comb.mul %c2_i32, %x : i32
    #     %1 = comb.add %c1_i32, %0 : i32
    #     %c3_i32 = hw.constant 3 : i32
    #     %2 = comb.mul %x, %x : i32
    #     %3 = comb.mul %c3_i32, %2 : i32
    #     %4 = comb.add %1, %3 : i32
    #     %c4_i32 = hw.constant 4 : i32
    #     %5 = comb.mul %x, %x, %x : i32
    #     %6 = comb.mul %c4_i32, %5 : i32
    #     %7 = comb.add %4, %6 : i32
    #     %c5_i32 = hw.constant 5 : i32
    #     %8 = comb.mul %x, %x, %x, %x : i32
    #     %9 = comb.mul %c5_i32, %8 : i32
    #     %10 = comb.add %7, %9 : i32
    #     msft.output %10 : i32
    #   }
    # }
    #
    #     """

    # TODO: think about how to do "get possible pass"
    # get_possible_pass(original_ir_code)
    sv_name_pattern = re.compile(r'(?:output_file\s*<|fileName\s*=\s*)"([^"]+\.sv)"')
    sv_possible_name_pattern = re.compile(r'@(\w+)|sym_name\s*=\s*"(.*?)"')
    # sv_possible_name_pattern = re.compile(r'@\w+')# This one pass 6226.mlir test
    # file = open(sys.argv[1], "r")
    # original_ir_code = file.read()
    # file.close()

    # initial_tracing_dict = location_information_parse(input_text_tracing=original_sv_code)

    minimized_ir_code = ddmin_ir(original_ir_code)
    print("Minimized IR code:")
    print(minimized_ir_code)  # minimized code saved into one mlir file: test.mlir
    print("compiler fault chain:")
    print(compiler_variants)
    # processes = [f'a{i}' for i in range(1, 101)]
