author__ = 'Alysa Obertas'
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
import os
import rebound
import sys

#######################################################################
## read in initial condition file

infile = 'initial_conditions.npz'

ic = np.load(infile)

outdir = str(ic['outdir'])

archive_flag = ic['archive_flag']
archive_interval = ic['archive_interval']

m_star = ic['m_star'] # mass of star
m_planet = ic['m_planet'] # mass of planets

Nsims = ic['Nsims']
Nbody = ic['Nbody'] # number of planets
year = 2 * np.pi # One year in units where G=1
tf = ic['tf'] # end time in years

a = ic['a'] # array containing initial semimajor axis for each delta,planet

rh = a[0][0] * (m_planet / 3) ** (1/3) # hill radius of innermost planet, for close encounter distance

