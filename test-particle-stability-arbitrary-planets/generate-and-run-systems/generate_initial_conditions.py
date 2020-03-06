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
# N_planets: number of massive planets
# test_particle_position: placement of test particle; 1 would be between planets 1 and 2, 2 between 2 and 3, etc.
# m_star: mass of the star (solar masses)
# m_planets: masses of planets (solar masses)
# m_test: mass of test particle - note: not a true test particle for simplicity (solar masses)
# P_ratios: period ratios relative to inner planet
# P_planets: periods of massive planets (REBOUND time)
# P_test_min: minimum period of test particle (REBOUND time)
# P_test_max: maximum period of test particle (REBOUND time)
# P_test_rand: periods for Nsims test particles (REBOUND time)
# e_min: lower bound for massive planets' eccentricites
# e_max: upper bound for massive planets' eccentricites
# e_rand: massive planets' eccentricites
# e_test: test particle eccentricity
# inc_min: lower bound for massive planets' inclinations (radians)
# inc_max: upper bound for massive planets' inclinations (radians)
# inc_rand: massive planets' inclinations (radians)
# inc_test: test particle inclination (radians)
# pomega_min: lower bound for massive planets' longitudes of pericentre (radians)
# pomega_max: upper bound for massive planets' longitudes of pericentre (radians)
# pomega_rand: massive planets' longitudes of pericentre (radians)
# pomega_test: test particle longitude of pericentre (radians)
# f_min: lower bound for massive planets' initial positions (radians)
# f_max: upper bound for massive planets' initial positions (radians)
# f_rand: imassive planets' initial positions (radians)
# f_test: test particle initial position (radians)
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

N_planets = 3 # number of massive planets

m_star = 1.0 # mass of star (solar masses)
m_earth = 3.0035e-6 # mass of earth (solar masses)
m_planets = np.array([3, 3, 3]) * m_earth # masses of planets (solar masses)

P_1 = 10 * day # orbit period of inner planet (REBOUND time)

P_ratio = 1.3 * golden_ratio

P_ratios = np.array([1, 1.3, 1.2 * 1.3]) # orbit period ratios relative to inner-most planet; first entry is 1 for inner planet

P_planets = P_ratios * P_1 # orbit periods of planets (REBOUND time)

#######################################################################
## simulation parameters

outdir = "/mnt/scratch-lustre/obertas/koi-systems-dynamical-packing/test-particle-stability-arbitrary-planets/" # root directory where simulation data files will be saved
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

e_min = 0 # lower bound for massive planets' orbital eccentricity
e_max = 0.1 # upper bound for massive planets' orbital eccentricity
e_rand = np.random.uniform(e_min, e_max, (N_planets,Nsims)) # massive planets' orbital eccentricities

inc_min = -5 * np.pi / 180 # lower bound for massive planets' orbital inclination (radians)
inc_max = 5 * np.pi / 180 # upper bound for massive planets' orbital inclination (radians)
inc_rand = np.random.uniform(inc_min, inc_max, (N_planets,Nsims)) # massive planets' orbital inclinations (radians)

pomega_min = 0 # lower bound for massive planets' orbital longitudes of pericentre (radians)
pomega_max = 2 * np.pi # upper bound for massive planets' orbital longitudes of pericentre (radians)
pomega_rand = np.random.uniform(pomega_min, pomega_max, (N_planets,Nsims)) # massive planets' orbital longitudes of pericentre (radians)

f_min = 0 # lower bound for massive planets' initial position (radians)
f_max = 2 * np.pi # upper bound for massive planets' initial position (radians)
f_rand = np.random.uniform(f_min, f_max, (N_planets,Nsims)) # massive planets' initial positions (radians)

#######################################################################
## test particle parameters

m_test = m_earth * 1e-3 # mass of test particle (solar masses)

test_particle_position = 0 # placement of test particle; 0 would be between planets 1 and 2, 1 between 2 and 3, etc.

P_test_min = P_planets[test_particle_position] # lower bound for test particle period (days)
P_test_max = P_planets[test_particle_position+1] # upper bound for test particle period (days)
P_test_rand = np.random.uniform(P_test_min,P_test_max,Nsims) # test particle periods (days)

e_test = 0 # test particle eccentricity

inc_test = 0 # test particle inclination (radians)

pomega_test = 0 # test particle longitude of pericentre (radians)

f_test = 0 # test particle initial position (radians)
    
#######################################################################
      
## save initial conditions to file

np.savez(outfile,outdir=outdir,job_pre=job_pre,archive_flag=archive_flag,archive_interval=archive_interval, \
                 Nsims=Nsims,N_planets=N_planets,test_particle_position=test_particle_position, \
                 m_star=m_star,m_planets=m_planets,m_test=m_test, \
                 P_1=P_1,P_ratios=P_ratios,P_planets=P_planets,P_test_min=P_test_min, \
                 P_test_max=P_test_max,P_test_rand=P_test_rand, \
                 e_min=e_min,e_max=e_max,e_rand=e_rand,e_test=e_test, \
                 inc_min=inc_min,inc_max=inc_max,inc_rand=inc_rand,inc_test=inc_test, \
                 pomega_min=pomega_min,pomega_max=pomega_max,pomega_rand=pomega_rand,pomega_test=pomega_test, \
                 f_min=f_min,f_max=f_max,f_rand=f_rand,f_test=f_test, \
                 t_max=t_max,steps_per_orbit=steps_per_orbit,dt=dt)
