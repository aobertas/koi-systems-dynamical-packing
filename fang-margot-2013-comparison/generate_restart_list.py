# python generate_restart_list.py file1 file2 output

import sys
import numpy as np

args = sys.argv
file1= str(args[1])
file2 = str(args[2])
output = str(args[3])

i=0

with open(file1, "r") as f:
    file1_data = f.readlines()

with open(file2, "r") as f:
    file2_data = f.readlines()

file1_data = np.array(file1_data)
file2_data = np.array([int(s.rstrip('\n')) for s in file2_data])

output_data = file1_data[file2_data]

with open(output, "a") as f:
    for line in output_data:
        f.write(line)