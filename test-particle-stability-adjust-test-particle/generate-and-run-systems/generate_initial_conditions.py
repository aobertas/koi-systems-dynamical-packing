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

# outdir: str(ic['outdir']) returns the string of the directory location where
#         files are to be saved (note: the str() seems to be necessary)
# job_pre: str(ic['job_pre') returns the string of the prefix for sunnyvale job name
# archive_flag: boolean (True/False) for whether rebound simulation archives are to be saved
# archive_interval: time interval between archive snapshots (REBOUND time)
# Nsims: number of simulations to be run
# m_star: mass of the star (solar masses)
# m_1: mass of inner planet (solar masses)
# m_2: mass of outer planet (solar masses)
# m_test: mass of test particle - note: not a true test particle for simplicity (solar masses)
# P_ratio: period ratio of outer:inner
# P_1: period of inner planet (REBOUND time)
# P_2: period of outer planet (REBOUND time)
# P_min: minimum period of test particle (REBOUND time)
# P_max: maximum period of test particle (REBOUND time)
# P_rand: periods for Nsims test particles (REBOUND time)
# e_1: eccentricity of inner planet
# e_2: eccentricity of outer planet
# e_min: minimum eccentricity of test particle
# e_max: maximum eccentricity of test particle
# e_rand: eccentricities for Nsims test particles
# inc_1: inclination of inner planet (radians)
# inc_2: inclination of outer planet (radians)
# inc_min: minimum inclination of test particle (radians)
# inc_max: maximum inclination of test particle (radians)
# inc_rand: inclinations for Nsims test particles (radians)
# pomega_1: longitude of periapsis of inner planet (radians)
# pomega_2: longitude of periapsis of outer planet (radians)
# pomega_min: minimum longitude of periapsis of test particle (radians)
# pomega_max: maximum longitude of periapsis of test particle (radians)
# pomega_rand: longitudes of periapsis for Nsims test particles (radians)
# t_max: maximum integration time (orbits)
# steps_per_orbit: integration time steps per orbit (of inner planet)
# dt: integration time step (REBOUND time)
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

outdir = "/mnt/scratch-lustre/obertas/koi-systems-dynamical-packing/test-particle-stability-adjust-test-particle/" # root directory where simulation data files will be saved
job_pre = "sim"

Nsims = 160000 # number of simulations

t_max = 1e9 # maximum integration time (orbits)

steps_per_orbit = 20 # timesteps per orbit of the inner planet
dt = P_1 / steps_per_orbit # WHFAST time step in REBOUND time

### CAUTION: SETTING BELOW TO True WILL SAVE VERY LARGE FILES TO DISK ###
archive_flag = False # whether or not to save intermediate info to simulation archive
archive_interval = 10000 * dt

#######################################################################
## test particle parameters

m_test = m_earth * 1e-3 # mass of test particle (solar masses)

P_min = P_1 # lower bound for test particle period (days)
P_max = P_2 # upper bound for test particle period (days)
P_rand = np.random.uniform(P_min,P_max,Nsims) # test particle periods (days)

e_min = 0 # lower bound for test particle eccentricity
e_max = 0.1 # upper bound for test particle eccentricity
e_rand = np.random.uniform(e_min,e_max,Nsims) # test particle eccentricities

inc_min = -5 * np.pi / 180 # lower bound for test particle inclination (radians)
inc_max = 5 * np.pi / 180 # upper bound for test particle inclination (radians)
inc_rand = np.random.uniform(inc_min,inc_max,Nsims) # test particle inclinations (radians)

pomega_min = 0 # lower bound for test particle longitude of pericentre (radians)
pomega_max = 2 * np.pi # upper bound for test particle longitude of pericentre (radians)
pomega_rand = np.random.uniform(pomega_min,pomega_max,Nsims) # test particle orbit longitudes of pericentre (radians)

# node_min = 0 # lower bound for test particle longitude of ascending node (radians)
# node_max = 2 * np.pi # upper bound for test particle longitude of ascending node (radians)
# node_rand = np.random.uniform(node_min,node_max,Nsims) # test particle longitudes of ascending node (radians)
    
#######################################################################
      
## save initial conditions to file

np.savez(outfile,outdir=outdir,job_pre=job_pre,archive_flag=archive_flag,archive_interval=archive_interval, \
                 Nsims=Nsims,m_star=m_star,m_1=m_1,m_2=m_2,m_test=m_test, \
                 P_ratio=P_ratio,P_1=P_1,P_2=P_2,P_min=P_min,P_max=P_max,P_rand=P_rand, \
                 e_1=e_1,e_2=e_2,e_min=e_min,e_max=e_max,e_rand=e_rand, \
                 inc_1=inc_1,inc_2=inc_2,inc_min=inc_min,inc_max=inc_max,inc_rand=inc_rand, \
                 pomega_1=pomega_1,pomega_2=pomega_2,pomega_min=pomega_min,pomega_max=pomega_max,pomega_rand=pomega_rand, \
                 t_max=t_max,steps_per_orbit=steps_per_orbit,dt=dt)
