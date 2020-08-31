__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python run_simulation.py filename
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
import sys

#######################################################################

def run_sim(filename):
    sa = rebound.SimulationArchive(filename)
    sim = sa[0]
    sim.integrator_synchronize() # need to manually sinchronize because safe_mode = 0

    P = sim.particles[1].P

    sim.automateSimulationArchive(filename, interval=1.e6*P)

    try:
        sim.integrate(1.e9*P, exact_finish_time=0)
    except (rebound.Collision or rebound.Escape): 
        sim.simulationarchive_snapshot(filename)

#######################################################################
## execute simulation

args = sys.argv
filename = str(args[1])

run_sim(filename)
