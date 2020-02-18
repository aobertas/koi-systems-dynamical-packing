__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python merge_output_files.py
#
# merges all numpy binary files located in outdir/files
#
# saves a combined file named
# merged_output_files.npz
#
# this information can be accessed by loading the file e.g.
# oc = np.load('merged_output_files.npz')
# 
# any information is easily accessed by its field name e.g.
# t_exit = ic['t_exit']
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
import numpy.matlib
import os

#######################################################################
## read in data file

infile = 'initial_conditions.npz'

ic = np.load(infile)

Nsims = ic['Nsims']
Nbody = ic['Nbody']

outdir = str(ic['outdir'])

#######################################################################
## data to save from each run

t_exit = np.zeros(Nsims) # array containing exit time for each beta, run

a_final = np.zeros((Nbody,Nsims))
e_final = np.zeros((Nbody,Nsims))

stop = np.zeros(Nsims)

#######################################################################
## data to save from each run

for i in range(Nsims):
    outfile = outdir + 'sim-' + str(i) + '.npz'
    oc = np.load(outfile)

    t_exit[i] = oc['t_exit']
    a_final[:,i] = oc['a_final']
    e_final[:,i] = oc['e']
    stop[i] = oc['stop']

merge_file = 'merged_output_files.npz'

np.savez(merge_file,t_exit=t_exit,a_final=a_final, e_final=e_final, stop=stop)
