__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python run_simulation.py nsim job_type
#
# run REBOUND simulation with initial condition determined by nsim
# won't work unless make_all_dirs.py has been run
#
# job_type is one of
#   initial: first time running simulation
#   restart: restart of simulation
#
# Written by Alysa Obertas

import rebound
import numpy as np
import sys

#######################################################################
## load initial conditions

infile = 'initial_conditions.npz'

ic = np.load(infile)

outdir = str(ic['outdir'])

archive_flag = ic['archive_flag']
archive_interval = ic['archive_interval']

m_star = ic['m_star'] # mass of star
m_planet = ic['m_planet'] # mass of planets

Nbody = ic['Nbody'] # number of planets
year = 2 * np.pi # One year in units where G=1
tf = ic['tf'] # end time in years
dt = ic['dt'] # time step in rebound time

a = ic['a'] # array containing initial semimajor axis for each delta,planet
f = ic['f'] # array containing intial longitudinal position for each delta, planet, run

rh = (m_planet / 3) ** (1./3) # hill radius of innermost planet, for close encounter distance

#######################################################################
## simulation function

def run_sim(nsim, job_type):

    outfile = outdir + "sim-" + str(nsim) + ".bin"
    close_encounter_list_file = "close_encounter_sim_list"

    max_int_time = tf * year

    if job_type == 'initial':

        sim = rebound.Simulation() # initialise simulation
        sim.add(m=m_star) # add star

        for i in range(Nbody): # add the planets
            sim.add(m=m_planet, a=a[i,nsim], f=f[i,nsim])
        
        sim.integrator = "whfast"
        sim.ri_whfast.safe_mode = 0
        sim.dt = dt
        sim.exit_min_distance = rh # close encounter distance 
        sim.move_to_com()

        # set up simulation archive based on flag
        if archive_flag:
            sim.automateSimulationArchive(outfile,interval=archive_interval,deletefile=True)
        else:
            sim.simulationarchive_snapshot(outfile)

            # note: in newer version of rebound, simulationarchive_snapshot can also take deletefile as 
            # a boolion argument and this would be better to implement for an initial run of a simulation

        # integrate system
        try:
            sim.integrate(max_int_time)
        except:
            with open(close_encounter_list_file, 'a') as ce_file:
                ce_file.write(str(nsim) + '\n')

        sim.simulationarchive_snapshot(outfile)
    elif job_type == 'restart':
        sim = rebound.Simulation(outfile)

        try:
            sim.integrate(sim.t + max_int_time)
        except:
            with open(close_encounter_list_file, 'a') as ce_file:
                ce_file.write(str(nsim) + '\n')

        sim.simulationarchive_snapshot(outfile)
    else:
        print('job_type is not one of initial or restart')

#######################################################################
## execute simulation

args = sys.argv
nsim = int(args[1])
job_type = str(args[2])

run_sim(nsim, job_type)
