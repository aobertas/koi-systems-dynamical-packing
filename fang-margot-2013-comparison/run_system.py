__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python run_simulation.py filename inttype
#
# Written by Alysa Obertas

import rebound
import numpy as np
import sys

#######################################################################

def run_sim(filename, inttype):
    sa = rebound.SimulationArchive(filename)
    sim = sa[0]
    sim.integrator_synchronize() # need to manually sinchronize because safe_mode = 0

    if inttype == "year":

        year = 2 * np.pi

        sim.automateSimulationArchive(filename, interval=1.e5*year)

        try:
            sim.integrate(1.e8*year, exact_finish_time=0)
        except rebound.Collision: 
            sim.simulationarchive_snapshot(filename)
        except rebound.Escape:
            sim.simulationarchive_snapshot(filename)
    elif inttype == "orbit":
        P = sim.particles[1].P

        sim.automateSimulationArchive(filename, interval=1.e6*P)

        try:
            sim.integrate(1.e9*P, exact_finish_time=0)
        except rebound.Collision: 
            sim.simulationarchive_snapshot(filename)
        except rebound.Escape:
            sim.simulationarchive_snapshot(filename)

#######################################################################
## execute simulation

args = sys.argv
filename = str(args[1])
inttype = str(args[2])

run_sim(filename, inttype)
