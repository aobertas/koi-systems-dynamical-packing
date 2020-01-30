__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python systems-predict-stability.py nsys first_sim p1 p2 p3
#
# predicts stability (for 1e9 orbits) of a 3+ planet system using machine learning
# method developed by Dan Tamayo
#
# finds probability for nsys systems, starting at first_sim
# examines triples from the 5 planet systems (p1, p2, p3)
# e.g. first set of adjacent triples is (1, 2, 3)
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
sys.path.append('../../../MLstability/generate_training_data')
from training_data_functions import ressummaryfeaturesxgbv6

np.random.seed(2)

#######################################################################
## machine learning stuff

folderpath = '../../../MLstability/'
model = 'ressummaryfeaturesxgbv6_resonant.pkl'

model, features, featurefolder = dill.load(open(folderpath+'/models/'+model, "rb"))

#######################################################################
## determine systems to run

args = sys.argv
nsys = int(args[1])
first_sim = int(args[2])
last_sim = first_sim + nsys - 1

p1 = int(args[3])
p2 = int(args[4])
p3 = int(args[5])

planet_list = [p1-1, p2-1, p3-1]

print('nsys = %d, first_sim = %d, p1 = %d, p2 = %d, p3 = %d' % (nsys, first_sim, p1, p2, p3))

if (first_sim < 16000) and (last_sim < 16000):
    nsim_list = np.arange(first_sim, last_sim+1)
    delta_set = 1
elif (first_sim >= 16000) and (last_sim >= 16000):
    nsim_list = np.arange(first_sim - 16000, last_sim - 16000 + 1)
    delta_set = 2
else:
    print('Simulations must be contained in the same initial condition file')
    print('first_sim and first_sim+nsys-1 should both be <16000 or >=16000')

outfile = '/mnt/raid-cita/obertas/github-repos/obertas-2017-systems-2019-ML-paper/\
ml-stability-prediction/triples/np-binary-files/stability-probs-sims-' + str(first_sim) \
+ '-to-' + str(last_sim) + '-planets-' + str(p1) + '-' + str(p2) + '-' + str(p3) + '.npz'

#######################################################################
## read initial condition file

infile_delta_2_to_10 = '/mnt/raid-cita/obertas/github-repos/obertas-2017-systems-2019-ML-paper\
/obertas-2017-paper-systems/initial_conditions_delta_2_to_10.npz'
infile_delta_10_to_13 = '/mnt/raid-cita/obertas/github-repos/obertas-2017-systems-2019-ML-paper\
/obertas-2017-paper-systems/initial_conditions_delta_10_to_13.npz'

if delta_set == 1:
    ic = np.load(infile_delta_2_to_10)
elif delta_set == 2:
    ic = np.load(infile_delta_10_to_13)
else:
    print('Simulations must be contained in the same initial condition file')
    print('first_sim and first_sim+nsys-1 should both be <16000 or >=16000')

m_star = ic['m_star'] # mass of star
m_planet = ic['m_planet'] # mass of planets
rh = (m_planet/3.) ** (1./3.)

Nbody = ic['Nbody'] # number of planets
year = 2.*np.pi # One year in units where G=1
tf = ic['tf'] # end time in years

a_init = ic['a'] # array containing initial semimajor axis for each delta,planet
f_init = ic['f'] # array containing intial longitudinal position for each delta, planet, run

#######################################################################
## create rebound simulation and predict stability for each system in nsim_list

system_stability_probs = []

for nsim in nsim_list:
    
    # make rebound simulation
    sim = rebound.Simulation()
    sim.add(m=m_star)

    for i in planet_list: # add the planets
        sim.add(m=m_planet, a=a_init[i,nsim], f=f_init[i,nsim]) #ignore for now: inc=np.random.rand(1)*1e-10, e=np.random.rand(1)*1e-10)
    sim.move_to_com()
    
    # summary features
    args = (10000, 1000) # (Norbits, Nout) Keep this fixed
    summaryfeatures = ressummaryfeaturesxgbv6(sim, args)
    
    if features is not None:
        summaryfeatures = summaryfeatures[features]
    summaryfeatures = pd.DataFrame([summaryfeatures]) # convert it to the pandas format model expects
    
    # predict probability
    probstability = model.predict_proba(summaryfeatures)[:, 1][0]
    system_stability_probs.append(probstability)
    
system_stability_probs = np.array(system_stability_probs)

np.savez(outfile, delta_set=delta_set,nsim_list=nsim_list, probs=system_stability_probs)
