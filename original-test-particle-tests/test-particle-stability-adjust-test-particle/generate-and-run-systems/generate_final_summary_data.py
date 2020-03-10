__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python generate_final_summary_data file_name
#
# generates a numpy binary file containing summary info from simulations
# saves to a file called file_name.npz
#
# this information can be accessed by loading the file e.g.
# fd = np.load('file_name.npz')
# 
# any information is easily accessed by its field name e.g.
# t_exit = fd['t_exit']
#
# list of fields:
# t_exit: array of size (len(nsims)) of time in years at the end of the last (successful) timestep (float)
# t_run: array of size (len(nsims)) of time in seconds that the simulation ran for on computer (float)
# a_final: array of size ((Nbody,len(nsims))) of final semimajor axes (floats)
# x: array of size ((Nbody,len(nsims))) of final position in AU on x-axis (floats)
# y: array of size ((Nbody,len(nsims))) of final position in AU on y-axis (floats)
# vx: array of size ((Nbody,len(nsims))) of final velocity in 2pi*AU/yr in x-direction (floats)
# vy: array of size ((Nbody,len(nsims))) of final velocity in 2pi*AU/yr in y-direction (floats)
# stop: array of size (len(nsims)) of flag determining whether simulation stopped at max integration time (0) or had a
#       close encounter (1) (integer)
# nsims: array of size (len(nsims)) of all simulation numbers contained in this merged set (integers)
#
# Written by Alysa Obertas

import numpy as np
import rebound
import sys

#######################################################################
## read initial condition file

infile = 'initial_conditions.npz'

ic = np.load(infile)

#Nsims = ic['Nsims']
Nbody = ic['Nbody']

outdir = str(ic['outdir'])

delta_all = ic['delta']

sim_list = np.arange(4000,12000)
Nsims = len(sim_list)

#######################################################################
## data to save from each simulation

t_exit = np.zeros(Nsims) # exit time for each simulation
delta = np.zeros(Nsims) # mutual hill radius for each simulation

#######################################################################
## data to save from each run

for i, nsim in enumerate(sim_list):
    outfile = outdir + 'sim-' + str(nsim) + '.bin'
    sim = rebound.Simulation(outfile)

    delta[i] = delta_all[nsim]
    t_exit[i] = sim.t / (2 * np.pi)

args = sys.argv
file_name = str(args[1])

np.savez(file_name+'.npz',t_exit=t_exit,delta=delta)
