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


def _find_most_probable_part(weights, parts):
    """ Find the most probable particle using their weights.
    
    Args:
        + *weights*: Normalized probability of observing a particle for each 
        particle.
        
        + *parts*: 3xNxM array of particles with observations and factors.
    
    Returns: 
        + *most_prob_parts: 3xN array containing most probable particle for
        each observation.
        
    """
    index_part = np.argmax(weights, axis=1)
    most_prob_part = np.empty(parts.shape[0:2])
    for i, index in enumerate(index_part):
        most_prob_part[:, i] = parts[:, i, index]
        
    return most_prob_part    
    
    
def particle_smoother():
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
    # Set up the factors and their type (non-constant or constant).
    f_nr = ['fac1', 'fac2', 'fac3']
    f_setting = [1, 1, 0]
    # Load in the measurement data.
    meas_objs = []
    for fac in f_nr:
        data = pd.read_pickle(ppj("OUT_ANALYSIS", 'meas_'+fac+'.pkl'))
        params_list = []
        for param_dic in meas_params:
            if fac == param_dic['factor']:
                params_list.append(param_dic)
        meas_objs.append(Measurement(params_list, data))
    # Set up transition equations.
    trans_params = json.load(
                             open(
                                     ppj("IN_MODEL_SPECS", "transitions.json"),
                                     encoding = "utf-8"
                                 )
                            )
    trans_obj = Transition(trans_params, f_setting)
    # History of resampled particles over periods.
    history = []
    # Load prior and transition errors.
    #prior = np.load(ppj("OUT_ANALYSIS", "prior_samples.pickle"))
    prior = np.load(ppj("OUT_ANALYSIS", "true_degenerated_prior.pickle"))
    trans_errors = np.load(ppj("OUT_ANALYSIS", "transition_errors.pickle"))
    # Auxiliary function for sampling.
    sampling = lambda distr : multinomial(params["n_particles"], distr)
    
    # Forward iteration of particle smoother.
    # ========================================
    history.append(prior)
    for per in range(params["period"]):
        next_state = trans_obj.next_state(
                                            history[per],
                                            trans_errors[:,:,per,:]
                                         )
        probs = np.zeros((params["obs"], params["n_particles"]))
        fac_to_consider = np.nonzero((np.array(f_setting)-.1)*per >= 0)[0]
        for i in fac_to_consider:
            # Take logs of probabilities to calculate product more easily.
            probs += np.log(meas_objs[i].marginal_probability(
                                                            next_state[i, ...],
                                                            per+1)
                                                             )
        particle_probs = np.exp(probs)
        weights = (
                    particle_probs / 
                    np.tile(
                             np.sum(particle_probs, axis = 1),
                             (params["n_particles"], 1)
                            ).T
                  )
        samples = np.apply_along_axis(sampling, 1, weights)
        # Construct drawn particles and save them in new array.
        history.append(_construct_new_particles(samples, next_state))
    
    # Backward iteration of particle smoother.
    # =========================================
    estimates = pd.DataFrame(
                     data = np.zeros((params["obs"]*params["period"], 3)),
                     columns = f_nr,
                     index = pd.MultiIndex.from_product([
                                                         range(1,params["obs"]+1),
                                                         range(1,params["period"]+1)
                                                     ]) 
                            )
    arr_est = _find_most_probable_part(weights, next_state)
    estimates.loc[(slice(None),params["period"]),:] = arr_est.T
    for per in reversed(range(1, params["period"])):
        weights = trans_obj.marginal_probability(arr_est, history[per])
        arr_est = _find_most_probable_part(weights, history[per])
        estimates.loc[(slice(None), per), :] = arr_est.T
    return estimates
    
if __name__ == "__main__":
    factors = particle_smoother()
    factors.to_pickle(ppj("OUT_ANALYSIS", "factor_estimates.pkl"))