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

        ps = sim.particles[1:]

        distances = np.array([p.d for p in ps])

        if np.all(distances < sim.exit_max_distance):
            close_encounters = 0
            for p in ps:
                spacing = np.array([np.sqrt((p.x - p2.x) ** 2 + (p.y - p2.y) ** 2 + (p.z - p2.z) ** 2) for p2 in ps])
                rsum = np.array([p.r + p2.r for p2 in ps])
                close_encounters = close_encounters + np.sum(spacing[spacing > 0] < rsum[spacing > 0])
            if close_encounters == 0:
                if sim.t < 1e8 * year:
                    resubmit_sys_list.append(filename)

    np.savetxt(outfile, np.array(resubmit_sys_list), fmt="%s")


#######################################################################
## execute simulation

args = sys.argv
dirname = str(args[1])
outfile = str(args[2])

run_sim(dirname, outfile)
