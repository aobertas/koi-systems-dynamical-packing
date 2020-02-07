__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python submit_jobs.py initial Njobs first_sim
# OR
# python submit_jobs.py restart sim_list_file
#
# submit jobs to sunnyvale queue
# 
# job_type is one of
#   initial: first time running a simulation
#   restart: restart of simulation
#
# For initial, number of jobs Njobs and the first simulation to run are required
# e.g. 'python submit_jobs.py initial 100 0' will submit jobs for simulations 
# with indices 0 to 99 (inclusive)
#
# For restart, a file with a list of simulations is required
# e.g. 'python subit_jobs.py restart sims_billion_orbits' will submit all simulations
# in the file 'sims_billion_orbits'
#
# Written by Alysa Obertas

import sys
import os
import numpy as np

infile = 'initial_conditions.npz'
ic = np.load(infile)
job_pre = str(ic['job_pre'])

args = sys.argv
job_type = str(args[1])

if job_type == 'initial':
    Njobs = int(args[2])
    first_sim = int(args[3])

    tmp_script_file = 'tmp_sunnyvale_job_submit_script'

    for i in range(Njobs):
        with open(tmp_script_file, 'w') as f:
            f_head = open('job_header','r')
            f.write(f_head.read())
            f.write('#PBS -l walltime=48:00:00' + '\n')
            f.write('#PBS -N ' + job_pre + str(i+first_sim) + '\n')
            f_mid = open('job_middle','r')
            f.write(f_mid.read())
            f_head.close()
            f_mid.close()
            f.write('python run_simulation.py ' + str(i+first_sim) + ' initial \n')
        os.system('qsub ' + tmp_script_file) # submit job to sunnyvale

elif job_type == 'restart':
    sim_list_file = str(args[2])
    sim_list = []

    with open(sim_list_file) as f:
        for line in f.readlines():
            sim_list.append(int(line))

    tmp_script_file = 'tmp_sunnyvale_job_submit_script'

    for sim in sim_list:
        with open(tmp_script_file, 'w') as f:
            f_head = open('job_header','r')
            f.write(f_head.read())
            f.write('#PBS -l walltime=48:00:00' + '\n')
            f.write('#PBS -N ' + job_pre + str(sim) + '\n')
            f_mid = open('job_middle','r')
            f.write(f_mid.read())
            f_head.close()
            f_mid.close()
            f.write('python run_simulation.py ' + str(sim) + ' restart \n')
        os.system('qsub ' + tmp_script_file) # submit job to sunnyvale

else:
    print('job_type is not one of initial or restart')
