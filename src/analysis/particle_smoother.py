"""
Analysis.

"""

import numpy as np
import pandas as pd
import json

import sys, os
os.getcwd()
sys.path.insert(0,'./../../bld/')
from project_paths import project_paths_join as ppj

#from bld.project_paths import project_paths_join as ppj
from measurement import Measurement
from transition import Transition
from numpy.random import multinomial

def _construct_new_particles(samples, old_particles):
    """Construct new array of particles given the drawing results over the old
    particles.
    
    Args:
        + *samples* (np.ndarray): NxM array that contains the drawing results,
            where N is number of observations and M number of particles.
        + *old_particles* (np.ndarray): 3xNxM array that stores old particles.
    
    Returns:
        + new particles (np.ndarray): 3xNxM array of newly assembled particles
            (for each observation, there will be repeated particles).
    """
    
    N, M = samples.shape
    ret_arr = 5*np.ones((3,N,M))
    m_outer = np.zeros(N)
    while 0 < np.amax(samples):
        indices = np.nonzero(samples)
        last_n = -1
        for i, n in enumerate(indices[0]):
            if last_n < n:
                if last_n >= 0:
                    m_outer[last_n] += m_inner
                m_inner = 0
            ret_arr[:,n,int(m_outer[n]+m_inner)] = old_particles[
                                                                 :,n,
                                                                 indices[1][i]
                                                                ]
            m_inner += 1
            last_n = n
        m_outer[last_n] += m_inner
        samples[indices] -= 1
    return ret_arr

if __name__ == "__main__":
    trans_params = json.load(
                             open(
                                     ppj("IN_MODEL_SPECS", "transitions.json"),
                                     encoding = "utf-8"
                                 )
                            )
    trans_obj = Transition(trans_params, [1, 1, 0])
    test_state = np.array([[[1, 7],[2, 5]],[[3, 8],[1, 3]],[[5, 9],[4, 2]]])
    test_errors = np.array([[[.5, .3],[-.1, .8]],[[-.3, -.2],[.1, -.5]]])
    test_next = trans_obj.next_state(test_state, test_errors)
    meas_params = json.load(
                             open(
                                    ppj("IN_MODEL_SPECS", "measurements.json"),
                                    encoding="utf-8"
                                 )
                            )
    f_nr = ['fac1', 'fac2', 'fac3']
    meas_objs = []
    for fac in f_nr:
        data = pd.read_pickle(ppj("OUT_ANALYSIS", 'meas_'+fac+'.pkl'))
        params = []
        for param_dic in meas_params:
            if fac == param_dic['factor']:
                params.append(param_dic)
        meas_objs.append(Measurement(params, data))
    probs = []
    test_facs = np.ones((4, 4000, 100))
    test_facs[0:3, ...] = np.array(list(range(-50, 50)))/100
    for i, fac in enumerate(f_nr):
        test_facs_df = pd.DataFrame(test_facs[i,...])
        # Take logs of probabilities to take product more easily.
        probs.append(np.log(meas_objs[i].marginal_probability(test_facs_df,1)))
    particle_probs = np.exp(sum(probs).values)
    # Save weights together with particles.
    test_facs[3, ...] = (
                         particle_probs / 
                         np.tile(np.sum(particle_probs, axis = 1), (100, 1)).T
                        )
    sampling = lambda distr : multinomial(100, distr)
    samples = np.apply_along_axis(sampling, 1, test_facs[3, ...])
    # Construct drawn particles and save them in new array.
    parts_constr = _construct_new_particles(samples, test_facs[0:3, ...])
        