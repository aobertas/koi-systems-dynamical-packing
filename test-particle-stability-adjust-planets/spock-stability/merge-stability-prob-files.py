__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python merge-stability-prob-files.py file_name infile_dir_name nsys
#
# merges all system probability numpy files into one single file
# file is called file_name.npz and nsys is the number of systems
# in each smaller file
#
# Written by Alysa Obertas

import numpy as np
import sys

#######################################################################
## setup

args = sys.argv
outfile = str(args[1])
infile_dir_name = str(args[2])
nsys = int(args[3])

infile_prefix = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
test-particle-stability-adjust-planets/spock-stability/np-binary-prediction-files/" + infile_dir_name + \
"/stability-probs-sims-"

#######################################################################
## merge numpy binary files

infile = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
test-particle-stability-adjust-planets/generate-and-run-systems/initial_conditions.npz"

ic = np.load(infile)

Nsims = ic['Nsims']

full_nsim_list = np.arange(Nsims)
full_probs = np.zeros(Nsims)

for first_sim in np.arange(0,Nsims,nsys):
    last_sim = first_sim + nsys - 1
    infile = infile_prefix + str(first_sim) + "-to-" + str(last_sim) + ".npz"
    data = np.load(infile)

    full_probs[first_sim:last_sim+1] = data['probs']

np.savez(outfile, nsim_list=full_nsim_list, probs=full_probs)