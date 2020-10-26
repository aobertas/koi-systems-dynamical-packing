# python generate_restart_list.py file1 file2 output

import sys

args = sys.argv
file1= str(args[1])
file2 = str(args[2])
output = str(args[3])

i=0

with open(file1, "r") as f:
    file1_data = f.read()

with open(file2, "r") as f:
    file2_data = f.read()

print(file1_data[0:10])

# with open(file2, "r") as f2:
#         with open(output, "a") as of:
#             while i < 20:
#                 archive_name = f1.readline()
#                 linenum = int(f2.readline().strip())

#                 while i <= linenum:

#                     print(archive_name, linenum, i)

#                     archive_name = f1.readline()
#                     # of.write(str(archive_name) + "\n")
#                     i += 1
