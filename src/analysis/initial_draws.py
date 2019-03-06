"""
In the file 'initial.draws.py, we construct the arguments to initialize the 
particler smoother analysis and store those elements.

The script transfers the fixed parameters of the analysis from several json 
files in "IN_MODEL_SPECS" directory. This feauture enables the code being 
easily adapted to different analysis.
    * smooth.json provides the number of observation, periods, particles as 
    well as the random seed set for the random drawings.
    * true_prior.json includes the variances for each factors' prior 
    distribution which is with mean zero and relevant variances.
    
Transition errors for transitions equations of factor 1 and factor 2 are 
generated for each observation, period and and particle combinations.

Samples of factors from prior distributions are created. For each observation,
100*100=10000 particles exist.

Tesulted arrays are stored as pickle files in "OUT_ANALYSIS" directory.

"""

import numpy as np
import json
import pickle
import pandas as pd

from bld.project_paths import project_paths_join as ppj


def transition_errors(fixed):
    """Generate the errors for transitions equations of factor 1 and factor 2.

    """    
    errors = np.random.normal(
                                0, 1, (
                                        2*fixed["obs"]*fixed["period"]*
                                            fixed["n_particles"]
                                    )
                            ).reshape(
                                         (2, fixed["obs"], fixed["period"], 
                                          fixed["n_particles"]
                                          )
                                     )
                    
    return errors
    

def cov_matrix(prior):
    """Load the parameters of true prior distribution to form the covariance 
    matrix.
    
    """
    var = []
    for d in prior:
        var = np.append(var, d["var_p"])
    cov_12 = np.array(
                    [(var[0], 0), (0, var[1])]   #diagonal covariances
             )
    return cov_12

def prior_samples(cov_12, prior, fixed):
    """Draw fac1 and fac2 from joint prior distribution and return the random 
    sample of fac1 and fac2.
    
    """
    mean = [0, 0]
    var3=prior[2]["var_p"]
    prior_sample=np.empty([3, fixed["obs"], (fixed["n_particles"])])
    total = np.zeros(((fixed["n_particles"]), 3))
    for i in range(0, (fixed["obs"]+1)):
        
        f12_0 = np.random.multivariate_normal(
                                             mean,cov_12,fixed["draws_varying"]
                                             ) 
        f3_0  = np.random.normal(0, var3, fixed["draws_constant"]) 
        total[:, 0:2] = np.array(f12_0.repeat(len(f3_0), axis=0))
        total[:, 2] = np.array(np.tile(f3_0, len(f12_0)))
        prior_sample[:, i:(i+1), :]= np.expand_dims(total.T, axis=1)
    
    return prior_sample
    
def _true_prior_samples(true_facs):
    """ Take true factors of period 1 as prior samples.
    
    """
    true_per_1 = ((true_facs.loc[(slice(None), 1), :]).values).T
    true_prior = np.repeat(
                    true_per_1[:, :, np.newaxis], fixed["n_particles"], axis=2
                        )
    
    return true_prior

if __name__ == "__main__":
    prior = json.load(
                      open(
                              ppj("IN_MODEL_SPECS", "true_prior.json"), 
                              encoding="utf-8"
                              )
                      )
    fixed = json.load(
                      open(
                              ppj("IN_MODEL_SPECS", "smoother.json"), 
                              encoding="utf-8"
                              )
                      )
    
    
    np.random.seed(fixed["rnd_seed"])
    true_facs= pd.read_pickle(ppj("OUT_ANALYSIS", "true_facs.pkl"))
    # Load true variances and form covarince matrix     
    cov_12 = cov_matrix(prior)
     #Draw random samples of fac1&fac2 and fac3. Merge those to form whole sample.
    prior_all = prior_samples(cov_12, prior, fixed)
    # Store the drawn samples.
    with open(ppj("OUT_ANALYSIS", "prior_samples.pickle"), "wb") as out_file:
        pickle.dump(prior_all, out_file)
    # Load true factors of period 1.
    true_prior = _true_prior_samples(true_facs)
    # Store the factors of period 1.
    with open(ppj("OUT_ANALYSIS", "true_degenerated_prior.pickle"), "wb") as out_file:
        pickle.dump(true_prior, out_file)
   # Construct errors for transition equations of fac1 and fac2.
    tr_errors = transition_errors(fixed)
    #Store errors as pickle file.
    with open(ppj("OUT_ANALYSIS", "transition_errors.pickle"), "wb") as out_file:
        pickle.dump(tr_errors, out_file)
        
        
    
        
    

