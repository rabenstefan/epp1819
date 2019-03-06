"""
Analysis.

"""

import numpy as np
import pandas as pd
import json

# =============================================================================
# import sys, os
# os.getcwd()
# sys.path.insert(0,'./../../bld/')
# from project_paths import project_paths_join as ppj
# =============================================================================

from bld.project_paths import project_paths_join as ppj
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
    params = json.load(
                        open(
                                ppj("IN_MODEL_SPECS", "smoother.json"),
                                encoding = "utf-8"
                             )
                    )
    np.random.seed(params["rnd_seed"])
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
        params_list = []
        for param_dic in meas_params:
            if fac == param_dic['factor']:
                params_list.append(param_dic)
        meas_objs.append(Measurement(params_list, data))
    trans_params = json.load(
                             open(
                                     ppj("IN_MODEL_SPECS", "transitions.json"),
                                     encoding = "utf-8"
                                 )
                            )
    trans_obj = Transition(trans_params, [1, 1, 0])
    # History of resampled particles over periods.
    history = []
    # Load prior and transition errors.
    prior = np.load(ppj("OUT_ANALYSIS", "prior_samples.pickle"))
    trans_errors = np.load(ppj("OUT_ANALYSIS", "transition_errors.pickle"))
    # Auxiliary function for sampling.
    sampling = lambda distr : multinomial(params["n_particles"], distr)
    f_nr_list = [f_nr[0:2] for i in range(params["period"])]
    f_nr_list[0] = f_nr
    
    history.append(prior)
    for per in range(params["period"]):
        next_state = trans_obj.next_state(
                                            history[per],
                                            trans_errors[:,:,per,:]
                                        )
        probs = []
        for i, fac in enumerate(f_nr_list[per]):
            state_df = pd.DataFrame(next_state[i, ...])
            # Take logs of probabilities to calculate product more easily.
            probs.append(np.log(meas_objs[i].marginal_probability(state_df,per+1)))
        particle_probs = np.exp(sum(probs).values)
        weights = (
                    particle_probs / 
                    np.tile(np.sum(particle_probs, axis = 1), (params["n_particles"], 1)).T
                  )
        samples = np.apply_along_axis(sampling, 1, weights)
        # Construct drawn particles and save them in new array.
        history.append(_construct_new_particles(samples, next_state))
        