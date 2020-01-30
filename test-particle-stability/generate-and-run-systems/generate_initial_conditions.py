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

golden_ratio = 1.618034
year = 2 * np.pi # one year in REBOUND time (in units where G=1)
day = year / 365 # one day in REBOUND time (in units where G=1)

#######################################################################
## systen/massive planet parameters

m_star = 1.0 # mass of star (solar masses)
m_earth = 3.0035e-6 # mass of earth (solar masses)
m_1 = 3 * m_earth # mass of inner planet (solar masses)
m_2 = 7 * m_earth # mass of outer planet (solar masses)

P_ratio = 1.3 * golden_ratio
P_1 = 10 * day # orbit period of inner planet (days)
P_2 = P_1 * P_ratio # orbit period of outer planet (days)

e_1 = 0.01 # eccentricity of inner planet
e_2 = 0.02 # eccentricity of outer planet

inc_1 = 1 * np.pi / 180 # inclination of inner planet (radians)
inc_2 = -1 * np.pi / 180 # inclination of outer planet (radians)

pomega_1 = 0 # orientation of inner planet orbit (radians)
pomega_2 = 100 * golden_ratio * np.pi / 180 # orientation of outer planet orbit (radians)

#######################################################################
## simulation parameters

outdir = "/mnt/scratch-lustre/obertas/koi-systems-dynamical-packing/test-particle-stability/" # root directory where simulation data files will be saved
job_pre = "sim"

Nsims = 10000 # number of simulations

t_max = 1e9 # maximum integration time (orbits)

steps_per_orbit = 20 # timesteps per orbit of the inner planet
dt = P_1 / steps_per_orbit # WHFAST time step in REBOUND time

### CAUTION: SETTING BELOW TO True WILL SAVE VERY LARGE FILES TO DISK ###
archive_flag = False # whether or not to save intermediate info to simulation archive
archive_interval = 10000 * dt

#######################################################################
## test particle parameters

m_test = m_earth * 1e-3 # mass of test particle (solar masses)

P_min = 1.2 * P_1 # lower bound for test particle period (days)
P_max = P_2 / 1.2 # upper bound for test particle period (days)
P_rand = np.random.uniform(P_min,P_max,Nsims) # test particle periods (days)
P_sort = np.sort(P_rand) # test particle periods, sorted in ascending order (days)

e_min = 0.005 # lower bound for test particle eccentricity
e_max = 0.05 # upper bound for test particle eccentricity
e_rand = np.random.uniform(e_min,e_max,Nsims) # test particle eccentricities
e_sort = np.sort(e_rand) # test particle eccentricities, sorted in ascending order

inc_min = -5 * np.pi / 180 # lower bound for test particle inclination (radians)
inc_max = 5 * np.pi / 180 # upper bound for test particle inclination (radians)
inc_rand = np.random.uniform(inc_min,inc_max,Nsims) # test particle inclinations (radians)
inc_sort = np.sort(inc_rand) # test particle inclinations, sorted in ascending order (radians)

pomega_min = 0 # lower bound for test particle orbit orientation (radians)
pomega_max = 2 * np.pi # upper bound for test particle orbit orientation (radians)
pomega_rand = np.random.uniform(pomega_min,pomega_max,Nsims) # test particle orbit orientations (radians)
pomega_sort = np.sort(e_rand) # test particle orbit orientations, sorted in ascending order (radians)
    
#######################################################################
      
## save initial conditions to file

np.savez(outfile,outdir=outdir,archive_flag=archive_flag,archive_interval=archive_interval,job_pre=job_pre, \
                 Nsims=Nsims,m_star=m_star,m_1=m_1,m_2=m_2,m_test=m_test, \
                 P_ratio=P_ratio,P_1=P_1,P_2=P_2,P_min=P_min,P_max=P_max,P_sort=P_sort, \
                 e_1=e_1,e_2=e_2,e_min=e_min,e_max=e_max,e_sort=e_sort, \
                 inc_1=inc_1,inc_2=inc_2,inc_min=inc_min,inc_max=inc_max,inc_sort=inc_sort, \
                 pomega_1=pomega_1,pomega_2=pomega_2,pomega_min=pomega_min,pomega_max=pomega_max,pomega_sort=pomega_sort, \
                 t_max=t_max,steps_per_orbit=steps_per_orbit,dt=dt)
