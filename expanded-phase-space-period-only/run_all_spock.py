__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python run_all_spock.py dirname outfile start n
#
#
# Written by Alysa Obertas

import rebound
import numpy as np
import glob
import spock
import sys

#######################################################################

def run_sim(dirname, outfile, start, n):

    model = spock.FeatureClassifier()

    system_stability_probs = []
    identifier_list = []
    file_list = sorted(glob.glob(dirname + "/*.bin"))

    stop = start + n

    for filename in file_list[start:stop]:
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
    np.savez(outfile + str(start) + ".npz", identifier_list=identifier_list, probs=system_stability_probs)

#######################################################################
## execute simulation

args = sys.argv
dirname = str(args[1])
outfile = str(args[2])
start = int(args[3])
n = int(args[4])

run_sim(dirname, outfile, start, n)
