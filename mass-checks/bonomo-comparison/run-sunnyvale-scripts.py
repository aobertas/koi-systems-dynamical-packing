#python run-sunnyvale-scripts.py dirname n_samp

import numpy as np
import pandas as pd
import sys
import os

#######################################################################
def run_sunnyvalue_scripts(df, dirname, n_samp):
    for sysid in df['kepid'].unique():
        N_planets = len(df[df['kepid'] == sysid])
        N_pair = N_planets - 1

        for i in range(N_pair):
            os.system("qsub -v sysid=" + str(sysid) + ",place=" + str(i) + \
                ",dirname=" + dirname + ",n_samp=" + str(n_samp) + \
                " sunnyvale-qsub-script-spock-probs")

#######################################################################

args = sys.argv
dirname = str(args[1])
n_samp = int(args[2])

df = pd.read_csv("../generate-tables/cumulative_koi_gaia_dr2.csv", comment="#")

run_sunnyvalue_scripts(df, dirname, n_samp)
