__author__ = 'Alysa Obertas'
__email__ = 'obertas@astro.utoronto.ca'

# python generate_initial_conditions.py ic_file
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
# P_test_min: minimum period of test particle (REBOUND time)
# P_test_max: maximum period of test particle (REBOUND time)
# P_test_rand: periods for Nsims test particles (REBOUND time)
# e_1_min: lower bound for inner planet eccentricity
# e_1_max: upper bound for inner planet eccentricity
# e_1_rand: inner planet eccentricities
# e_2_min: lower bound for outer planet eccentricity
# e_2_max: upper bound for outer planet eccentricity
# e_2_rand: outer planet eccentricities
# e_test: test particle eccentricity
# inc_1_min: lower bound for inner planet inclination (radians)
# inc_1_max: upper bound for inner planet inclination (radians)
# inc_1_rand: inner planet inclinations (radians)
# inc_2_min: lower bound for outer planet inclination (radians)
# inc_2_max: upper bound for outer planet inclination (radians)
# inc_2_rand: outer planet inclinations (radians)
# inc_test: test particle inclination (radians)
# pomega_1_min: lower bound for inner planet longitude of pericentre (radians)
# pomega_1_max: upper bound for inner planet longitude of pericentre (radians)
# pomega_1_rand: inner planet longitudes of pericentre (radians)
# pomega_2_min: lower bound for outer planet longitude of pericentre (radians)
# pomega_2_max: upper bound for outer planet longitude of pericentre (radians)
# pomega_2_rand: outer planet longitudes of pericentre (radians)
# pomega_test: test particle longitude of pericentre (radians)
# t_max: maximum integration time (orbits)
# steps_per_orbit: integration time steps per orbit (of inner planet)
# dt: integration time step (REBOUND time)
#
# Written by Alysa Obertas

import numpy as np
import sys

np.random.seed(2) # seed random number generator

#######################################################################
## fixed system/massive planet parameters

args = sys.argv
outfile = str(args[1])

outfile = "initial-conditions-" + outfile + ".npz" # initial condition file

golden_ratio = 1.618034
year = 2 * np.pi # one year in REBOUND time (in units where G=1)
day = year / 365 # one day in REBOUND time (in units where G=1)

#######################################################################
## fixed system/massive planet parameters

m_star = 1.0 # mass of star (solar masses)
m_earth = 3.0035e-6 # mass of earth (solar masses)
m_1 = 3 * m_earth # mass of inner planet (solar masses)
m_2 = 7 * m_earth # mass of outer planet (solar masses)

P_ratio = 1.383
P_1 = 10 * day # orbit period of inner planet (days)
P_2 = P_1 * P_ratio # orbit period of outer planet (days)

#######################################################################
## simulation parameters

outdir = "/mnt/scratch-lustre/obertas/koi-systems-dynamical-packing/test-particle-stability-test-Omega/" # root directory where simulation data files will be saved
job_pre = "sim"

Nsims = 160000 # number of simulations

t_max = 1e9 # maximum integration time (orbits)

steps_per_orbit = 20 # timesteps per orbit of the inner planet
dt = P_1 / steps_per_orbit # WHFAST time step in REBOUND time

### CAUTION: SETTING BELOW TO True WILL SAVE VERY LARGE FILES TO DISK ###
archive_flag = False # whether or not to save intermediate info to simulation archive
archive_interval = 10000 * dt

#######################################################################
## varied massive planet parameters

e_1_min = 0 # lower bound for inner planet eccentricity
e_1_max = 0.1 # upper bound for inner planet eccentricity
e_1_rand = np.random.uniform(e_1_min,e_1_max,Nsims) # inner planet eccentricities

e_2_min = 0 # lower bound for outer planet eccentricity
e_2_max = 0.1 # upper bound for outer planet eccentricity
e_2_rand = np.random.uniform(e_2_min,e_2_max,Nsims) # outer planet eccentricities

inc_1_min = -5 * np.pi / 180 # lower bound for inner planet inclination (radians)
inc_1_max = 5 * np.pi / 180 # upper bound for inner planet inclination (radians)
inc_1_rand = np.random.uniform(inc_1_min,inc_1_max,Nsims) # inner planet inclinations (radians)

inc_2_min = -5 * np.pi / 180 # lower bound for outer planet inclination (radians)
inc_2_max = 5 * np.pi / 180 # upper bound for outer planet inclination (radians)
inc_2_rand = np.random.uniform(inc_2_min,inc_2_max,Nsims) # outer planet inclinations (radians)

pomega_1_min = 0 # lower bound for inner planet longitude of pericentre (radians)
pomega_1_max = 2 * np.pi # upper bound for inner planet longitude of pericentre (radians)
pomega_1_rand = np.random.uniform(pomega_1_min,pomega_1_max,Nsims) # inner planet longitudes of pericentre (radians)

pomega_2_min = 0 # lower bound for outer planet longitude of pericentre (radians)
pomega_2_max = 2 * np.pi # upper bound for outer planet longitude of pericentre (radians)
pomega_2_rand = np.random.uniform(pomega_2_min,pomega_2_max,Nsims) # outer planet longitudes of pericentre (radians)

#######################################################################
## test particle parameters

m_test = m_earth * 1e-3 # mass of test particle (solar masses)

P_test_min = P_1 # lower bound for test particle period (days)
P_test_max = P_2 # upper bound for test particle period (days)
P_test_rand = np.random.uniform(P_test_min,P_test_max,Nsims) # test particle periods (days)

e_test = 0 # test particle eccentricity

inc_test = 0 # test particle inclination (radians)

# note: pomega_test is set for the sake of consistency, but it is UNDEFINED for a circular orbit
pomega_test = 0 # test particle longitude of pericentre (radians)
    
#######################################################################
      
## save initial conditions to file

np.savez(outfile,outdir=outdir,job_pre=job_pre,archive_flag=archive_flag,archive_interval=archive_interval, \
                 Nsims=Nsims,m_star=m_star,m_1=m_1,m_2=m_2,m_test=m_test, \
                 P_ratio=P_ratio,P_1=P_1,P_2=P_2,P_test_min=P_test_min,P_test_max=P_test_max,P_test_rand=P_test_rand, \
                 e_1_min=e_1_min,e_1_max=e_1_max,e_2_min=e_2_min,e_2_max=e_2_max, \
                 e_1_rand=e_1_rand,e_2_rand=e_2_rand,e_test=e_test, \
                 inc_1_min=inc_1_min,inc_1_max=inc_1_max,inc_2_min=inc_2_min,inc_2_max=inc_2_max, \
                 inc_1_rand=inc_1_rand,inc_2_rand=inc_2_rand,inc_test=inc_test, \
                 pomega_1_min=pomega_1_min,pomega_1_max=pomega_1_max,pomega_2_min=pomega_2_min,pomega_2_max=pomega_2_max, \
                 pomega_1_rand=pomega_1_rand,pomega_2_rand=pomega_2_rand,pomega_test=pomega_test, \
                 t_max=t_max,steps_per_orbit=steps_per_orbit,dt=dt)
