__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python systems-predict-stability.py ic_file nsys first_sim
#
# predicts stability (for 1e9 orbits) of a 2 planet + test particle system
#
# finds probability for nsys systems, starting at first_sim
#
# Written by Alysa Obertas (modified from code written by Dan Tamayo)

import numpy as np
import rebound
import matplotlib.pyplot as plt
import matplotlib
import random
import dill
import sys
import pandas as pd
import spock

np.random.seed(2)

#######################################################################
## determine systems to run

args = sys.argv
ic_file = str(args[1])
nsys = int(args[2])
first_sim = int(args[3])
last_sim = first_sim + nsys - 1

nsim_list = np.arange(first_sim, last_sim+1)

print("nsys = %d, first_sim = %d" % (nsys, first_sim))

outfile = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
two-planet-sample-param-space/spock-stability/np-binary-probability-files/"\
+ ic_file + "/stability-probs-sims-" + str(first_sim) + "-to-" + str(last_sim) + ".npz"

#######################################################################
## read initial condition file

infile = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
two-planet-sample-param-space/generate-and-run-systems/initial-conditions-" + ic_file + ".npz"

ic = np.load(infile)

N_planets = ic['N_planets'] # number of massive planets
test_particle_position = ic['test_particle_position'] # placement of test particle

m_star = ic['m_star'] # mass of star (solar masses)
m_planets = ic['m_planets'] # masses of planets (solar masses)
m_test = ic['m_test'] # mass of test particle (solar masses)

P_planets = ic['P_planets'] # periods of massive planets (REBOUND time)
P_test_rand = ic['P_test_rand'] # periods for Nsims test particles (REBOUND time)

e_rand = ic['e_rand'] # massive planets' eccentricities
e_test = ic['e_test'] # test particle eccentricity

inc_rand = ic['inc_rand'] # massive planets' inclinations (radians)
inc_test = ic['inc_test'] # test particle inclination (radians)

pomega_rand = ic['pomega_rand'] # massive planets' longitude of pericentre (radians)
pomega_test = ic['pomega_test'] # test particle longitude of pericentre (radians)

f_rand = ic['f_rand'] # massive planets' initial positions (radians)
f_test = ic['f_test'] # test particle initial position (radians)

#######################################################################
## create rebound simulation and predict stability for each system in nsim_list

model = spock.StabilityClassifier()

system_stability_probs = []

for nsim in nsim_list:
    
    # make rebound simulation
    sim = rebound.Simulation()
    sim.add(m=m_star)

    for i in range(N_planets):
        sim.add(m=m_planets[i], P=P_planets[i], e=e_rand[nsim, i], inc=inc_rand[nsim, i], \
                pomega=pomega_rand[nsim, i], f=f_rand[nsim, i])
    sim.add(m=m_test, P=P_test_rand[nsim], e=e_test, inc=inc_test, pomega=pomega_test, f=f_test)
    sim.move_to_com()
    
    # predict probability
    probstability = model.predict(sim, copy=False)
    system_stability_probs.append(probstability)
    
system_stability_probs = np.array(system_stability_probs)

np.savez(outfile, nsim_list=nsim_list, probs=system_stability_probs)
