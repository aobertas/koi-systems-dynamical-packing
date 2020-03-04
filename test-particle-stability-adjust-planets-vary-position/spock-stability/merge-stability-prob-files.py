__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python merge-stability-prob-files.py ic_file outfile nsys
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
ic_file= str(args[1])
outfile = str(args[2])
nsys = int(args[3])

probs_file_prefix = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
test-particle-stability-planets-vary-position/spock-stability/np-binary-probability-files/"\
+ ic_file + "/stability-probs-sims-"

#######################################################################
## merge numpy binary files

infile = "/mnt/raid-cita/obertas/github-repos/koi-systems-dynamical-packing/\
test-particle-stability-planets-vary-position/generate-and-run-systems/initial-conditions-" + ic_file + ".npz"

ic = np.load(infile)

Nsims = ic['Nsims']

full_nsim_list = np.arange(Nsims)
full_probs = np.zeros(Nsims)

for first_sim in np.arange(0,Nsims,nsys):
    last_sim = first_sim + nsys - 1
    infile = probs_file_prefix + str(first_sim) + "-to-" + str(last_sim) + ".npz"
    data = np.load(infile)

    full_probs[first_sim:last_sim+1] = data['probs']

np.savez(outfile, nsim_list=full_nsim_list, probs=full_probs)