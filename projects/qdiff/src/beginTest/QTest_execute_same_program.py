

logfile = open("../testing record.txt","w+")
import transitionBackend.acrossbackendCirq as acC
import transitionBackend.acrossbackendPyquil as acP
import transitionBackend.acrossbackendQiskit as acQ
import os,sys,shutil
import compare.KScompare as cR
import mutation.Mutation_diff as diff_m
import beginTest.check_qubit_number as q_number
import re,random

def execution(pyfile_name:str):
    try:
        os.system('python3.7 ' + pyfile_name)
    except Exception as e:
        print("OS error:" + str(e))
        print("Save document as:" + pyfile_name)



def backend_loop(out_num:int):
    #print("Executing Simulator" + str(out_num))
    print("Executing Simulator" + str(out_num),file=logfile)

    #execution('../benchmark/' + "startCirq" + str(out_num) + ".py")
    #execution('../benchmark/' + "startPyquil" + str(out_num) + ".py")
    execution('../benchmark/' + "startQiskit" + str(out_num) + ".py")



def calculate_results(out_num:int, directory:str):
    wrong, diff, name = cR.compare("../"+directory, thershold=thershold,
                                   qubit_number=q_number.check("../benchmark/" + "startCirq" + str(out_num) + ".py"))

    if len(wrong)==0:
        return diff
    else:
        print("Wrong Output Detect:", wrong)
        print("Wrong Output Detect:", wrong,file=logfile)
        print("Name:",name)
        print("Name:", name,file=logfile)
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

    thershold = 0.15


    n = 100
    tail = 1
    seed = 0
    max_now = 0
    text_list = []

    text_list.append(0)

    while tail < n:

        j = 0

        print("Generating Same Program at number"+str(tail),file=logfile)
        #print("Generating Same Program at number" + str(tail))
        text_list.append(tail)
        diff_m.same(text_list[seed],tail)
        tail = tail +1


        backend_loop(text_list[seed])
        flag_see_wrong = 0

        while j < 100:

            j = j + 1
            print("now we are at round:", seed,file=logfile)
            #print("now we are at round:", seed)
            diff_m.same(text_list[seed], tail)
            backend_loop(tail)
            #diff = calculate_results(tail,"data")
            #if diff>thershold:
            #    flag_see_wrong = 1

            #if diff > max_now:
            #    max_now = diff
            #    text_list.append(tail)

            #print("K-S Diff:", max_now, file=logfile)
            #print("K-S Diff:", max_now)

            tail = tail + 1

        diff = calculate_results(tail-1, "data")
        if diff > max_now:
            max_now = diff
            text_list.append(tail)

        print("K-S Diff:", max_now)
        print("K-S Diff:", max_now, file=logfile)

        collect_data(seed,flag_see_wrong,"data")
        #collect_data(seed,flag_see_wrong,"data/reverse")

        seed = seed + 1

        if seed > len(text_list):
            seed = random.randint(seed-1)

    logfile.close()

