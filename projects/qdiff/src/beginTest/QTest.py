

"""
TODO: Add threshold for each quantum computer on circuit length

"""


Framework=['Cirq','Qiskit','Pyquil']
Cirq_t = [0.118,0.079,0.060,0.044,0.030,0.025]
Qiskit_t = [0.090,0.079,0.057,0.046,0.029,0.026]
Pyquil_t = [0.102,0.084,0.062,0.042,0.028,0.023]
logfile = open("../testing record.txt","w+")
twoq_gate_number = -1
import transitionBackend.acrossbackendCirq as acC
import transitionBackend.acrossbackendPyquil as acP
import transitionBackend.acrossbackendQiskit as acQ
import transitionBackend.Qiskitbackend
import transitionBackend.Pyquilbackend
import transitionBackend.Cirqbackend
import os,shutil
import compare.KScompare as cR
import compare.threshold_repetition
import mutation.Mutation_diff as diff_m
import mutation.Mutation_equal as equal_m
import mutation.Mutation_reverse as reverse_m
import beginTest.check_qubit_number as q_number
import re,random
import mutation.Mutation_must_diff as must_diff_m
import compare.compare

def execution(pyfile_name:str,reason:str):
    try:
        os.system('python3.7 ' + pyfile_name)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyfile_name)
        print("Bugs in" + reason)


def read_max_qubit_state(address:str, qubit_number:int)->(float,float):

    def trans_str(qubit_number: int, number: int) -> str:

        results = bin(number)
        results = results[2:len(results)]

        return results.zfill(qubit_number)

    def trans(data: str, flag_upside: int):  # flag1: to check if the bit order is upside down. Bit order for qiskit and pyquil classical are different
        result = re.split(',|}', data)
        final_data = []
        qubit_nonzero_state = 0


        for i in range(0, pow(2, qubit_number)):
            if flag_upside == 0:
                pattern = re.compile(trans_str(qubit_number,i) + "':")
            else:
                pattern = re.compile(''.join(reversed(trans_str(qubit_number,i))) + "':")
            flag = 0
            for results in result:
                s = re.search(pattern, results)
                if s is not None:
                    final_data.append(float(results[s.span()[1]:]))
                    flag = 1
                    qubit_nonzero_state += 1
                    break
            if flag == 0:
                final_data.append(0)

        return final_data, qubit_nonzero_state

    filename = address
    pattern_qiskit = re.compile("Qiskit")
    pattern_pyquilc = re.compile("Pyquil_Class")
    flag1 = 0
    pattern_result = re.compile("end")

    with open(filename, 'r') as f:
        print("Now read:" + filename)
        if (re.search(pattern_pyquilc, filename) is not None) or (re.search(pattern_qiskit, filename) is not None):
            flag1 = 1
        line = f.readline()

        end_file = line
        while end_file:
            end_file = f.readline()
            if pattern_result.search(end_file) is not None:
                break
            line = line + end_file
        data, qubit_state = trans(line, flag1)


        end_file = f.readline()
        length = float(end_file)
        print(length)

        circuit = f.readline()
        end_file = circuit
        while end_file:
            end_file = f.readline()
            circuit += end_file


    return max(data), qubit_state, length, circuit

def filter(circuit:str, two_qgate_number_ini:int, circuit_depth:int, threshold_circuit_depth:int, threshold2gate:int)->int:
    two_qpattern = re.compile('■')
    result =  two_qpattern.findall(circuit)
    if circuit_depth>threshold_circuit_depth:
        return -1
    if two_qgate_number_ini == -1:
        return result.__len__()
    if abs(result.__len__()-two_qgate_number_ini)>threshold2gate:
        return -1
    return 0



def backend_loop(out_num:int, queue:[]):

    #cirqP1, cirqP2, cirqP3 = acC.generate("../benchmark/" + "startCirq" + str(out_num) + ".py", "startCirq" + str(out_num) + ".py", out_num)
    #pyquilP1, pyquilP2 = acP.generate("../benchmark/" + "startPyquil" + str(out_num) + ".py", "startPyquil" + str(out_num) + ".py", out_num)
    qiskitP1, qiskitP2, qiskitP3 = acQ.generate("../benchmark/" + "startQiskit" + str(out_num) + ".py", "startQiskit" + str(out_num) + ".py", out_num)

    print("Executing Classical" + str(out_num))
    print("Executing Classical" + str(out_num),file=logfile)

    #execution('../benchmark/' + cirqP2,"state-vector")
    #execution('../benchmark/' + pyquilP2,"state-vector")
    execution('../benchmark/' + qiskitP2,"state-vector")

    max_p, qubit_state, circuit_length, circuit_picture = read_max_qubit_state("../data/" + "startQiskit_Class" + str(out_num) + ".csv", qubit_number) #get max_p and qubit number, and then get repetition number
    repetition_number = compare.threshold_repetition.KSRepetition(max_p=max_p,qubit_state_number=qubit_state,threshold=thershold_const).repetition()
    print("number of trail:",repetition_number)
    for circuits in queue:
        if circuits.__eq__(circuit_picture):
            print("Same circuit, skip!!")
            return "same"

    '''
    filter_flag = filter(circuit=circuit_picture,two_qgate_number_ini=twoq_gate_number,circuit_depth=round(circuit_length),threshold_circuit_depth=100,threshold2gate=10)<0
    if filter_flag<0:
        return "filtered"
    elif filter_flag>0:
        global twoq_gate_number
        twoq_gate_number = filter_flag
    '''
    #repetition_number = 5200 #should be change;
    qiskitP0 = transitionBackend.Qiskitbackend.change_repetition("../benchmark/startQiskit" + str(out_num) + ".py",repetition_number) #change repetition number
    qiskitP1 = transitionBackend.Qiskitbackend.change_repetition("../benchmark/"+qiskitP1,repetition_number)
    qiskitP3 = transitionBackend.Qiskitbackend.change_repetition("../benchmark/"+qiskitP3,repetition_number)

    #cirqP0 = transitionBackend.Cirqbackend.change_repetition("../benchmark/startCirq" + str(out_num) + ".py", repetition_number)
    #cirqP1 = transitionBackend.Cirqbackend.change_repetition("../benchmark/" + cirqP1, repetition_number)
    #cirqP3 = transitionBackend.Cirqbackend.change_repetition("../benchmark/" + cirqP3, repetition_number)

    #print("Executing Simulator" + str(out_num))
    #print("Executing Simulator" + str(out_num),file=logfile)

    #execution('../benchmark/' + cirqP0,"quantum-simulator")
    #execution('../benchmark/' + "startPyquil" + str(out_num) + ".py","quantum-simulator")
    #execution('../benchmark/' + qiskitP0,"quantum-simulator")

    #print("Executing compiler setting" + str(out_num))
    #print("Executing compiler setting" + str(out_num),file=logfile)
    print("Executing noisy simulation" + str(out_num))
    print("Executing noisy simulation" + str(out_num), file=logfile)

    #execution('../benchmark/' + cirqP1,"compilerSetting")
    #execution('../benchmark/' + pyquilP1,"compilerSetting")
    execution('../benchmark/' + qiskitP1,"noisy simulation")


    #print("Executing noisy simulation" + str(out_num))
    #print("Executing noisy simulation" + str(out_num),file=logfile)
    print("Executing quantum computer" + str(out_num))
    print("Executing quantum computer" + str(out_num), file=logfile)


    # execution('../benchmark/' + cirqP3,"noisy simulation")
    # execution('../benchmark/' + pyquilP3,"state-vector")
    execution('../benchmark/' + qiskitP3, "quantum-computer")

    """
    print("Executing reversion version of each program")
    print("Executing reversion version of each program",file=logfile)

    
    execution(reverse_m.generate_reverse('../benchmark/' + "startCirq" + str(out_num) + ".py",
                                         "../benchmark/reverse/"+ "startCirq" + str(out_num) + ".py"))
    execution(reverse_m.generate_reverse('../benchmark/' + "startPyquil" + str(out_num) + ".py",
                                         "../benchmark/reverse/" + "startPyquil" + str(out_num) + ".py"))
    execution(reverse_m.generate_reverse('../benchmark/' + "startQiskit" + str(out_num) + ".py",
                                         "../benchmark/reverse/" + "startQiskit" + str(out_num) + ".py"))

    execution(reverse_m.generate_reverse('../benchmark/' + cirqP1,'../benchmark/reverse/' + cirqP1))
    execution(reverse_m.generate_reverse('../benchmark/' + cirqP2,'../benchmark/reverse/' + cirqP2))
    execution(reverse_m.generate_reverse('../benchmark/' + pyquilP1, '../benchmark/reverse/' + pyquilP1))
    execution(reverse_m.generate_reverse('../benchmark/' + pyquilP2, '../benchmark/reverse/' + pyquilP2))
    execution(reverse_m.generate_reverse('../benchmark/' + qiskitP1, '../benchmark/reverse/' + qiskitP1))
    execution(reverse_m.generate_reverse('../benchmark/' + qiskitP2, '../benchmark/reverse/' + qiskitP2))
    """

    return circuit_picture

def calculate_results(directory:str,qubit_number:int):
    KScompare = compare.compare.KSScore(address="../"+directory ,qubit_number=qubit_number,threshold=thershold_const)

    wrong, diff, name = cR.compare("../"+directory, thershold=thershold_const,
                                   qubit_number=qubit_number)


    print(wrong,diff,name)

    if len(wrong)==0:
        return diff
    else:
        print("Wrong Output Detect:", wrong)
        print("Wrong Output Detect:", wrong,file=logfile)
        print("Name:",name)
        print("Name:", name,file=logfile)
        print("Bugs in compiler")
        return diff

def collect_data(num:int,flag:int,directory:str):

    right_file = re.compile("start")
    files = os.listdir("../"+directory+"/")
    if flag==1:
        dir_name = directory+"/Wrong"
    else:
        dir_name = directory+'/'

    if os.path.exists("../"+directory+"/"+str(num)) is True:
        shutil.rmtree("../"+directory+"/"+str(num))

    os.mkdir("../"+dir_name + str(num))

    for file in files:
        if (not os.path.isdir(file)) & (right_file.search(file) is not None):
            shutil.move("../"+directory+"/"+str(file),"../"+dir_name+str(num))


if __name__ == '__main__':

    #thershold_const= Cirq_t[1]

    thershold_const = 0.1
    total_identical_circuit = 0

    n = 2000
    tail = 1
    seed = 0
    max_now = 0
    program_list = []

    program_list.append(0)

    while tail < n:
        circuit_queue = []
        j = 0 #https://en.wikipedia.org/wiki/Sequential_probability_ratio_test

        print("Generating New Program at number"+str(tail),file=logfile)
        print("Generating New Program at number" + str(tail))
        program_list.append(tail)
        tail = tail + diff_m.mutate(program_list[seed], tail, "Cirq")#diff_m.mutate will return 0 if something goes wrong

        qubit_number = q_number.check("../benchmark/" + "startCirq" + str(program_list[seed]) + ".py")
        new_circuit=backend_loop(program_list[seed], queue=circuit_queue)
        if new_circuit!="same":
            circuit_queue.append(new_circuit)
            total_identical_circuit+=1

        flag_see_wrong = 0
        twoq_gate_number = -1



        while j < 10:

            j = j + 1
            print("Generating Equivalent Program for number" + str(program_list[seed]) + "at" + str(tail), file=logfile)
            print("Generating Equivalent Program for number" + str(program_list[seed]) + "at" + str(tail))
            equal_m.mutate(program_list[seed], tail)
            print("now we are at round:", seed,file=logfile)
            print("now we are at round:", seed)
            new_circuit = backend_loop(tail, queue=circuit_queue) # execute programs on each backends
            if new_circuit != "same":
                circuit_queue.append(new_circuit)
                total_identical_circuit += 1
            else:
                tail = tail + 1
                continue

            #diff = max(calculate_results(tail,"data"),calculate_results(tail,"data/reverse"))
            qubit_number = q_number.check("../benchmark/" + "startCirq" + str(tail) + ".py")
            diff = calculate_results("data",5)#qubit_number) # calculate the K-S statics
            print("K-S Diff:", diff,file=logfile)
            print("K-S Diff:", diff)
            if diff > thershold_const:
                flag_see_wrong = 1

            if diff > max_now:
                max_now = diff
                program_list.append(tail)

            tail = tail + 1

        """
        qubit_number = q_number.check("../benchmark/" + "startCirq" + str(seed) + ".py") #invoke must-different mutation
        must_diff_m.mutate(text_list[seed],tail,"Cirq")
        backend_loop(tail)
        diff = calculate_results("data",qubit_number)
        tail = tail+1
        if diff > thershold_const/qubit_number:
            print("Must different mutation makes different!")
            print("Must different mutation makes different!",file=logfile)
        else:
            print("Must different mutation failed!")
            print("Must different mutation failed!",file=logfile)
            flag_see_wrong = 1
        """

        collect_data(seed,flag_see_wrong,"data")
        #collect_data(seed,flag_see_wrong,"data/reverse")

        seed = seed + 1

        if seed > len(program_list):
            seed = random.randint(seed-1)

        print("Identical circuit:",total_identical_circuit)
        print("Identical circuit:",total_identical_circuit, file=logfile)

        print("total circuit:", tail)
        print("total circuit:", tail, file=logfile)

    print("Identical circuit:", total_identical_circuit)
    print("Identical circuit:", total_identical_circuit, file=logfile)
    logfile.close()

