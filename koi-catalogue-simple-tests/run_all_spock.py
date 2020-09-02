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
import spock
import sys

#######################################################################

def run_sim(dirname, outfile):

    model = spock.FeatureClassifier()

    system_stability_probs = []
    identifier_list = []

    for filename in glob.glob(dirname + "/*.bin"):
        identifier = filename.split('system-')[1].split('.bin')[0]
        identifier_list.append(identifier)

        sa = rebound.SimulationArchive(filename)
        sim = sa[0]
        sim.integrator_synchronize() # need to manually sinchronize because safe_mode = 0

        try:
            probstability = model.predict_stable(sim)
        except rebound.Escape:
            probability = 0.0
        system_stability_probs.append(probstability)

    system_stability_probs = np.array(system_stability_probs)
    np.savez(outfile, identifier_list=identifier_list, probs=system_stability_probs)

#######################################################################
## execute simulation

args = sys.argv
dirname = str(args[1])
outfile = str(args[2])

run_sim(dirname, outfile)
