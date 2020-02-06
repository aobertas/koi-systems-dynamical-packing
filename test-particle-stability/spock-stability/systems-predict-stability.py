__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python systems-predict-stability.py nsys first_sim
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
nsys = int(args[1])
first_sim = int(args[2])
last_sim = first_sim + nsys - 1

nsim_list = np.arange(first_sim, last_sim+1)

print("nsys = %d, first_sim = %d" % (nsys, first_sim))

outfile = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
test-particle-stability/spock-stability/np-binary-prediction-files/\
stability-probs-sims-" + str(first_sim) + "-to-" + str(last_sim) + ".npz"

#######################################################################
## read initial condition file

infile = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
test-particle-stability/generate-and-run-systems/initial_conditions.npz"

ic = np.load(infile)

m_star = ic['m_star'] # mass of star (solar masses)
m_1 = ic['m_1'] # mass of inner planet (solar masses)
m_2 = ic['m_2'] # mass of outer planet (solar masses)
m_test = ic['m_test'] # mass of test particle (solar masses)

P_1 = ic['P_1'] # period of inner planet (REBOUND time)
P_2 = ic['P_2'] # period of outer planet (REBOUND time)
P_rand = ic['P_sort'] # periods for Nsims test particles (REBOUND time)

e_1 = ic['e_1'] # eccentricity of inner planet
e_2 = ic['e_2'] # eccentricity of outer planet
e_rand = ic['e_sort'] # eccentricities for Nsims test particles

inc_1 = ic['inc_1'] # inclination of inner planet (radians)
inc_2 = ic['inc_2'] # inclination of outer planet (radians)
inc_rand = ic['inc_sort'] # inclinations for Nsims test particles (radians)

pomega_1 = ic['pomega_1'] # longitude of periapsis of inner planet (radians)
pomega_2 = ic['pomega_2'] # longitude of periapsis of outer planet (radians)
pomega_rand = ic['pomega_sort'] # longitudes of periapsis for Nsims test particles (radians)

#######################################################################
## create rebound simulation and predict stability for each system in nsim_list

model = spock.StabilityClassifier()

system_stability_probs = []

for nsim in nsim_list:
    
    # make rebound simulation
    sim = rebound.Simulation()
    sim.add(m=m_star)

    sim.add(m=m_1, P=P_1, e=e_1, inc=inc_1, pomega=pomega_1)
    sim.add(m=m_2, P=P_2, e=e_2, inc=inc_2, pomega=pomega_2)
    sim.add(m=m_test, P=P_rand[nsim], e=e_rand[nsim], inc=inc_rand[nsim], pomega=pomega_rand[nsim])
    sim.move_to_com()
    
    # predict probability
    probstability = model.predict(sim, copy=False)
    system_stability_probs.append(probstability)
    
system_stability_probs = np.array(system_stability_probs)

np.savez(outfile, nsim_list=nsim_list, probs=system_stability_probs)
