"""
Analysis.

"""

import numpy as np
import pandas as pd
import logging 
import json
import sys
import logging
import pickle

from bld.project_paths import project_paths_join as ppj


    
def cov_matrix(prior):
    """Load the parameters of true prior distribution to form the covariance 
    matrix, and load the seeds for random number generation.

    """
    var = np.array([]) 
    for d in prior:
        var = np.append(var, d["var_p"])
    
    cov_12 = np.array(
            [(var[0], 0), (0, var[1])]
            )
    return cov_12

def prior_sample(cov_12, var, rnd_seed, ):
    """Draw fac1 and fac2 from joint prior distribution and return the random 
    sample of fac1 and fac2.
    
    """
    
    mean = [0, 0]
    f12_0 = np.random.multivariate_normal(mean, cov_12, 4000)
    f3_0  = np.random_normal(0, var[3], 4000)
    
    return


   
# =============================================================================
# def run_analysis(agents, model):
#     """Given an initial set of *agents* and the *model*'s parameters,
#     return a list of dictionaries with *type: N x 2* items.
# 
#     """
# 
#     locations_by_round = [_get_locations_by_round_dict(model)]
#     _store_locations_by_round(locations_by_round[-1], agents)
# 
#     for loop_counter in range(model["max_iterations"]):
#         logging.info("Entering loop {}".format(loop_counter))
#         # Make room for locations.
#         locations_by_round.append(_get_locations_by_round_dict(model))
#         # Update locations as necessary
#         someone_moved = False
#         for agent in agents:
#             old_location = agent.location
#             # If necessary, move around until happy
#             agent.move_until_happy(agents)
#             if not (agent.location == old_location).all():
#                 someone_moved = True
#         _store_locations_by_round(locations_by_round[-1], agents)
#         # We are done if everybody is happy.
#         if not someone_moved:
#             break
# 
#     if someone_moved:
#         logging.info("No convergence achieved after {} iterations".format(model["max_iterations"]))
# 
#     return locations_by_round
# 
# =============================================================================

if __name__ == "__main__":
    prior = json.load(open(ppj("IN_MODEL_SPECS", "true_prior.json"), encoding="utf-8"))
    
    for d in prior:
        rnd_seed = d["rnd_seed"]
    
    np.random.seed=rnd_seed
    
    cov_12 = cov_matrix(prior)
    logging.basicConfig(
            filename=ppj("OUT_ANALYSIS", "log", "particle_smoother.log"),
            filemode="w",
            )
    
    logging.info(prior)

# =============================================================================
#     # Load initial locations and setup agents
#     agents = setup_agents(model)
#     # Run the main analysis
#     locations_by_round = run_analysis(agents, model)
#     # Store list with locations after each round
#     with open(ppj("OUT_ANALYSIS", "schelling_{}.pickle".format(model_name)), "wb") as out_file:
#         pickle.dump(locations_by_round, out_file)
# 
# =============================================================================

