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
test-particle-stability-test-Omega/spock-stability/np-binary-prediction-files/"\
+ ic_file + "/stability-probs-sims-" + str(first_sim) + "-to-" + str(last_sim) + ".npz"

#######################################################################
## read initial condition file

infile = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
test-particle-stability-test-Omega/generate-and-run-systems/initial-conditions-" + ic_file + ".npz"

ic = np.load(infile)

m_star = ic['m_star'] # mass of star (solar masses)
m_1 = ic['m_1'] # mass of inner planet (solar masses)
m_2 = ic['m_2'] # mass of outer planet (solar masses)
m_test = ic['m_test'] # mass of test particle (solar masses)

P_1 = ic['P_1'] # period of inner planet (REBOUND time)
P_2 = ic['P_2'] # period of outer planet (REBOUND time)
P_test_rand = ic['P_test_rand'] # periods for Nsims test particles (REBOUND time)

e_1_rand = ic['e_1_rand'] # inner planet eccentricities
e_2_rand = ic['e_2_rand'] # outer planet eccentricities
e_test = ic['e_test'] # test particle eccentricity

inc_1_rand = ic['inc_1_rand'] # inner planet inclinations (radians)
inc_2_rand = ic['inc_2_rand'] # outer planet inclinations (radians)
inc_test = ic['inc_test'] # test particle inclination (radians)

pomega_1_rand = ic['pomega_1_rand'] # inner planet longitude of pericentre (radians)
pomega_2_rand = ic['pomega_2_rand'] # outer planet longitude of pericentre (radians)
# note: pomega_test is set for the sake of consistency, but it is UNDEFINED for a circular orbit
pomega_test = ic['pomega_test'] # test particle longitude of pericentre (radians)

Omega_1_rand = ic['Omega_1_rand'] # inner planet longitude of ascending node (radians)
Omega_2_rand = ic['Omega_2_rand'] # outer planet longitude of ascending node (radians)
Omega_test = ic['Omega_test'] # test particle longitude of ascending node (radians)

#######################################################################
## create rebound simulation and predict stability for each system in nsim_list

model = spock.StabilityClassifier()

system_stability_probs = []

for nsim in nsim_list:
    
    # make rebound simulation
    sim = rebound.Simulation()
    sim.add(m=m_star)

    sim.add(m=m_1, P=P_1, e=e_1_rand[nsim], inc=inc_1_rand[nsim], pomega=pomega_1_rand[nsim], Omega=Omega_1_rand[nsim])
    sim.add(m=m_2, P=P_2, e=e_2_rand[nsim], inc=inc_2_rand[nsim], pomega=pomega_2_rand[nsim], Omega=Omega_2_rand[nsim])
    sim.add(m=m_test, P=P_test_rand[nsim], e=e_test, inc=inc_test, pomega=pomega_test, Omega=Omega_test)
    sim.move_to_com()
    
    # predict probability
    probstability = model.predict(sim, copy=False)
    system_stability_probs.append(probstability)
    
system_stability_probs = np.array(system_stability_probs)

np.savez(outfile, nsim_list=nsim_list, probs=system_stability_probs)
