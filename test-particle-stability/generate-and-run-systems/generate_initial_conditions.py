__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python generate_initial_conditions.py
#
# outputs a numpy compressed binary file (.npz) which contains simulation parameters
# and the initial conditions of the simulation
#
# this information can be accessed by loading the file e.g.
# ic = np.load('initial_conditions.npz')
# 
# any information is easily accessed by its field name e.g.
# Nsims = ic['Nsims']
#
# list of fields:
# outdir: str(ic['Nsims']) returns the string of the directory location where
#         files are to be saved (note: the str() seems to be necessary)
# job_pre: str(ic['job_pre') returns the string of the prefix for sunnyvale job name
# Nbody: number of planets in the system (integer)
# Nsims: number of simulations in the file (integer)
# m_star: mass of the star in stellar masses (float)
# m_planet: mass of the planets in stellar masses (float) (note: equal masses)
# delta: array of size (Nsims) of initial separations (floats)
# a: array of size ((Nbody,Nsims)) of initial semimajor axes (floats)
# f: array of size ((Nbody,Nsims)) of initial true anomalies (floats)
# tf: maximum integration time in years (float)
# spo: time steps per orbit of inner planet (float)
# dt: time step corresponding to period of inner planet divided by spo in REBOUND time (float)
# archive_flag: whether or not to save simulation to archive at archive_interval intervals (boolean)
# archive_interval: time in between archive snapshots (float)
#
# Written by Alysa Obertas

import numpy as np

np.random.seed(2) # seed random number generator
outfile = 'initial_conditions.npz' # initial condition file

#######################################################################
## simulation and system parameters

outdir = "/mnt/scratch-lustre/obertas/obertas-2017-systems-2019-ML-paper/" # root directory where simulation data files will be saved
job_pre = "5b"

m_star = 1.0 # mass of star (solar masses)
m_planet = 3.0035e-6 # mass of planets (solar masses)

Nsims = 16000 # number of simulations
delta_min = 2. # minimum initial spacing (mutual hill radii)
delta_max = 10. # maximum initial spacing

delta_rand = np.random.uniform(delta_min,delta_max,Nsims) # initial spacing of planets in mutual hill radii
delta_sort = np.sort(delta_rand) # sorted in ascending order

Nbody = 5 # number of planets
year = 2 * np.pi # One year REBOUND time (in units where G=1)
tf = 1e9 # maximum integration time (years)
steps_per_orbit = 20 # timesteps per orbit of the inner planet

a1 = 0.99 # semimajor axis of inner planet (AU)
dt = year / steps_per_orbit # WHFAST time step in REBOUND time

### CAUTION: SETTING BELOW TO True WILL SAVE VERY LARGE FILES TO DISK ###
archive_flag = False # whether or not to save intermediate info to simulation archive
archive_interval = 10000 * dt

#######################################################################
## initialise orbital parameters

a_init_all = np.zeros((Nbody,Nsims)) # array containing initial semimajor axis for each (planet, simulation)
f_init_all = np.random.uniform(0.0,2.0*np.pi,(Nbody,Nsims)) # array containing intial longitudinal position for each (planet, simulation)

#######################################################################
## calculate initial period and longitudinal angle of planets

X = 0.5 * (2. * m_planet / (3. * m_star)) ** (1./3) # eq. 4 from Obertas+(2017)

for i in range(Nsims):

    delta = delta_sort[i] # value of period ratio for this simulation

    # semimajor axis

    a_init = np.zeros(Nbody) # array of initial semimajor axes
    a_init[0] = a1

    for j in range(Nbody-1): # iteratively calculate periods
        a_init[j+1] = a_init[j] * (1 + delta * X) / (1 - delta * X) # eq. 9 from Obertas+(2017)

    a_init_all[:,i] = a_init
    
#######################################################################
      
## save initial conditions to file

np.savez(outfile,outdir=outdir,Nbody=Nbody,Nsims=Nsims,tf=tf,m_star=m_star,m_planet=m_planet, \
                 delta=delta_sort,a=a_init_all,f=f_init_all,spo=steps_per_orbit,dt=dt, \
                 archive_flag=archive_flag,archive_interval=archive_interval,job_pre=job_pre)
