#python generate-rebound-simulation-archives.py dirname n_samp

import numpy as np
import pandas as pd
import rebound
import mr_forecast as mr
import os
import sys
np.random.seed(2)

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
            
    return mr.Rpost2M([prad], unit='Earth', grid_size=1e3, classify='No') * m_earth

def get_sim_system(sysid):
    
    system = df[df['kepid'] == sysid].sort_values(by='koi_period')
    
    sim = rebound.Simulation()
    sim.add(m=system['koi_smass'].iloc[0])

    return sim, system

def insert_planet(df, sysid, sim, system, dirname, n_samp):

    N_rad = len(df['koi_prad'])
    
    sys_dirname = dirname + "system-" + str(sysid) + "/"
    os.mkdir(sys_dirname)
    
    m_earth = 3e-6
    year = 2 * np.pi # one year in REBOUND time (in units where G=1)
    day = year / 365 # one day in REBOUND time (in units where G=1)
    
    N_planets = len(system)
    N_pair = N_planets - 1

    periods = np.zeros(N_planets)
    prad = np.zeros(N_planets)
    prad_err1 = np.zeros(N_planets)
    prad_err2 = np.zeros(N_planets)

    j=0
    for i, planet in system.iterrows():
        periods[j] = planet['koi_period'] * day
        prad[j] = planet['koi_prad']
        prad_err1[j] = planet['koi_prad_err1']
        prad_err2[j] = planet['koi_prad_err2']
        j+=1
    
    for i in range(N_pair):
        place_dirname = sys_dirname + "place-" + str(i) + "/"
        os.mkdir(place_dirname)
        
        for j in range(n_samp):
            archive_name = place_dirname + "run-" + str(j) + ".bin"
            
            new_sim = sim.copy()
            
            for k in range(N_planets):
                pmass = single_pmass(prad[k], prad_err1[k], prad_err2[k])
                new_sim.add(m=pmass, P=periods[k], e=np.random.rayleigh(0.05), \
                            inc=(np.sign(2 * np.random.random() - 1) * np.random.rayleigh(0.03)), \
                            pomega="uniform", Omega="uniform", f="uniform")

            P_insert = np.random.uniform(new_sim.particles[i+1].P, new_sim.particles[i+2].P)
            m_insert = mr.Rpost2M([df['koi_prad'].iloc[np.random.randint(N_rad)]], \
                                unit='Earth', grid_size=1e3, classify='No') * m_earth
            
            new_sim.add(m=m_insert, P=P_insert, e=np.random.rayleigh(0.05), \
                        inc=(np.sign(2 * np.random.random() - 1) * np.random.rayleigh(0.03)), \
                        pomega="uniform", Omega="uniform", f="uniform")
        
            ps = new_sim.particles[1:]
        
            maxd = np.array([p.d for p in ps]).max()
            new_sim.exit_max_distance = 100*maxd

            for p in ps:
                p.r = p.rhill
            
            new_sim.move_to_com()
            new_sim.collision="line"
            new_sim.integrator="whfast"
            new_sim.dt = 0.05*ps[0].P
            new_sim.ri_whfast.safe_mode=0
        
            new_sim.save(archive_name)
        
    return None

def generate_archives(df, dirname, n_samp):

    for sysid in df['kepid'].unique()[0:20]:
        sim, system = get_sim_system(sysid)
        insert_planet(df, sysid, sim, system, dirname, n_samp)

#######################################################################

args = sys.argv
dirname = str(args[1])
n_samp = int(args[2])

df = pd.read_csv("../generate-tables/cumulative_koi_gaia_dr2.csv", comment="#")

generate_archives(df, dirname, n_samp)
