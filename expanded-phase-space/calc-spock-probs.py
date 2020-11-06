#python calc-spock-probs.py sysid place dirname n_samp

import numpy as np
import pandas as pd
import rebound
import spock
import mr_forecast as mr
import sys
import random

#######################################################################

def single_pmass(prad, err1, err2):
    m_earth = 3e-6
    
    if np.random.random() < 0.5:
        prad_rand = np.random.normal(prad, err1)
        if prad_rand < prad:
            prad_rand = 2 * prad - prad_rand
    else:
        prad_rand = np.random.normal(prad, err2)
        if prad_rand > prad:
            prad_rand = 2 * prad - prad_rand

    if prad_rand < 1e-1:
        prad_rand = 1e-1
    
    if prad_rand > 1e2:
        prad_rand = 1e2
            
    return mr.Rpost2M([prad_rand], unit='Earth', grid_size=1000, classify='No') * m_earth

def insert_planet(df, sysid, place):

    m_earth = 3e-6
    year = 2 * np.pi # one year in REBOUND time (in units where G=1)
    day = year / 365 # one day in REBOUND time (in units where G=1)

    system = df[df['kepid'] == sysid].sort_values(by='koi_period')

    N_rad = len(df['koi_prad'])

    sim = rebound.Simulation()
    sim.add(m=system['koi_smass'].iloc[0])

    for i, planet in system.iterrows():
        period = planet['koi_period'] * day
        prad = planet['koi_prad']
        prad_err1 = planet['koi_prad_err1']
        prad_err2 = planet['koi_prad_err2']

        pmass = single_pmass(prad, prad_err1, prad_err2)
        sim.add(m=pmass, P=period, e=np.random.rayleigh(0.05), inc=np.random.rayleigh(0.03), \
                omega="uniform", Omega="uniform", f="uniform")

    P_insert = np.random.uniform(sim.particles[place+1].P, sim.particles[place+2].P)
    m_insert = mr.Rpost2M([df['koi_prad'].iloc[np.random.randint(N_rad)]], \
                                unit='Earth', grid_size=1000, classify='No') * m_earth
    sim.add(m=m_insert, P=P_insert, e=np.random.rayleigh(0.05), inc=np.random.rayleigh(0.03), \
            omega="uniform", Omega="uniform", f="uniform")
        
    ps = sim.particles[1:]
        
    maxd = np.array([p.d for p in ps]).max()
    sim.exit_max_distance = 100*maxd

    for p in ps:
        p.r = p.rhill
            
    sim.move_to_com()
    sim.collision="line"
        
    return sim

def calc_spock_prob(sim, model):
    try:
        prob = model.predict_stable(sim)
    except rebound.Escape:
        prob = 0.0
    return prob

def get_spock_probs(df, sysid, place, dirname, n_samp):
    random.seed(sysid + place)
    np.random.seed(sysid + place)

    model = spock.FeatureClassifier()

    N_planets = len(df[df['kepid'] == sysid]) + 1

    prob = np.zeros(n_samp)
    mass = np.zeros((N_planets, n_samp))
    period = np.zeros((N_planets, n_samp))
    eccentricity = np.zeros((N_planets, n_samp))
    inclination = np.zeros((N_planets, n_samp))
    omega = np.zeros((N_planets, n_samp))
    Omega = np.zeros((N_planets, n_samp))
    f = np.zeros((N_planets, n_samp))


    for i in range(n_samp):
        sim = insert_planet(df, sysid, place)

        for j, p in enumerate(sim.particles[1:]):
            mass[j, i] = p.m
            period[j, i] = p.P
            eccentricity[j, i] = p.e
            inclination[j, i] = p.inc
            omega[j, i] = p.omega
            Omega[j, i] = p.Omega
            f[j, i] = p.f

        prob[i] = calc_spock_prob(sim, model)

    outfile = dirname + "spock-probs-system-" + str(sysid) + "-" + str(place) + ".npz"

    np.savez(outfile, prob=prob, mass=mass, period=period, eccentricity=eccentricity, \
        inclination=inclination, omega=omega, Omega=Omega, f=f)

    return None

#######################################################################

args = sys.argv
sysid = int(args[1])
place = int(args[2])
dirname = str(args[3])
n_samp = int(args[4])

df = pd.read_csv("../generate-tables/cumulative_koi_gaia_dr2.csv", comment="#")

get_spock_probs(df, sysid, place, dirname, n_samp)
