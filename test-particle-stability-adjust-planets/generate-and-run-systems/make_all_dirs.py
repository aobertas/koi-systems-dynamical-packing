__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python make_all_dirs.py
#
# run after generating initial conditions to make all necessary directories
# the sunnyvale job files can be put into a separate directory to avoid clutter
# the simulation output files are put into a separate directory
# note: on sunnyvale, I need to save to scratch-lustre to avoid file writing errors
#
# Written by Alysa Obertas

import numpy as np
import os

#######################################################################
## load initial conditions

infile = 'initial_conditions.npz'

ic = np.load(infile)

outdir = str(ic['outdir'])

#######################################################################
## make directories

os.system("mkdir job_files")
os.system("mkdir " + outdir)
