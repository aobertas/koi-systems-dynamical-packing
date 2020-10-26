# python generate_restart_list.py file1 file2 output

import sys

args = sys.argv
file1= str(args[1])
file2 = str(args[2])
output = str(args[3])

i=0

with open(file1, "r") as f1:
    with open(file2, "r") as f2:
        with open(output, "a") as of:
            while i < 920:
                archive_name = f1.readline()
                linenum = f2.readline().strip()

                print(linenum)

                # if linenum == i:
                #     of.write(str(archive_name) + "\n")
                # else:
                #     f1.readline()
                i += 1
