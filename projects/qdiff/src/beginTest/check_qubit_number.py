
import re

def check(address_in:str):

    readfile = open(address_in)
    qubit_number_patter = re.compile("# qubit number=")

    line = readfile.readline()
    print(address_in)
    while line:
        if qubit_number_patter.search(line):
            qubit_number = int(line[qubit_number_patter.search(line).span()[1]:])
            readfile.close()
            return qubit_number
        line = readfile.readline()
