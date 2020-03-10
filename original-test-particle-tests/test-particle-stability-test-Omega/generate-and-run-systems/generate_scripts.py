__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python generate_scripts.py
#
# generate scripts to submit jobs to sunnyvale
# won't work unless make_all_dirs.py has been run
# 
# Written by Alysa Obertas

import numpy as np
import sys


infile = 'initial_conditions.npz'
ic = np.load(infile)
job_pre = str(ic['job_pre'])

Nsims = ic['Nsims']

for i in range(Nsims):

    sh_script_name = 'job_scripts/sim-' + str(i)

    with open(sh_script_name, 'w') as f:
        f_head = open('job_header','r')
        f.write(f_head.read())            
        f.write('#PBS -l walltime=48:00:00' + '\n')
        f.write('#PBS -N ' + job_pre + str(i) + '\n')
        f_mid = open('job_middle','r')
        f.write(f_mid.read())
        f_head.close()
        f_mid.close()
        f.write('python run_simulation.py ' + str(i) + ' \n')            

    f.close()
