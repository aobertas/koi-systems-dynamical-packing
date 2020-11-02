# python generate_restart_list.py file1 file2 output
#
# generate file name using
# awk 'FNR==3 {if($0!="Collision"&&$0!="Escape") print FILENAME}' run-* > file_list
# awk '{split($0, a, "-", subs); split(a[2], b, ".", subs); print b[1]}' file_list > file_lines
# sort -n file_lines > file_lines_sorted

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