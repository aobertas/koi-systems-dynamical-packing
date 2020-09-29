__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python run_all_spock.py dirname outfile
#
# run REBOUND simulation with initial condition determined by nsim
# won't work unless make_all_dirs.py has been run
#
# job_type is one of
#   initial: first time running simulation
#   restart: restart of simulation
#
# Written by Alysa Obertas

import rebound
import numpy as np
import glob
import sys

#######################################################################

def run_sim(dirname, outfile):

    year = 2 * np.pi

    resubmit_sys_list = []

    for filename in glob.glob(dirname + "/*.bin"):

        sa = rebound.SimulationArchive(filename)
        sim = sa[-1]
    
        if sim.t < 1e8 * year:
            resubmit_sys_list.append(filename)

    np.savetxt(outfile, np.array(resubmit_sys_list), fmt="%s")


#######################################################################
## execute simulation

args = sys.argv
dirname = str(args[1])
outfile = str(args[2])

run_sim(dirname, outfile)
