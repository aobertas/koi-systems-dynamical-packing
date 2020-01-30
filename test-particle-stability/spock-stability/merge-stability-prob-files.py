__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python merge-stability-prob-files.py file_name nsys
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
outfile_prefix = str(args[1])
nsys = int(args[2])

infile_prefix = '/mnt/raid-cita/obertas/github-repos/obertas-2017-systems-2019-ML-paper/\
ml-stability-prediction/triples/np-binary-files/stability-probs-sims-'

#######################################################################
## merge numpy binary files

triples_list = [(1,2,3), (1,2,4), (1,2,5), (1,3,4), (1,3,5), (1,4,5), \
    (2,3,4), (2,3,5), (2,4,5), (3,4,5)]

for triple in triples_list:
    p1 = triple[0]
    p2 = triple[1]
    p3 = triple[2]

    file_suffix = '-planets-' + str(p1) + '-' + str(p2) + '-' + str(p3) + '.npz'

    outfile = outfile_prefix + file_suffix

    full_nsim_list = np.arange(17500)
    full_probs = np.zeros(17500)

    for first_sim in np.arange(0,17500,nsys):
        last_sim = first_sim + nsys - 1
        infile = infile_prefix + str(first_sim) + '-to-' + str(last_sim) + file_suffix
        data = np.load(infile)

        full_probs[first_sim:last_sim+1] = data['probs']

    np.savez(outfile, nsim_list=full_nsim_list, probs=full_probs)