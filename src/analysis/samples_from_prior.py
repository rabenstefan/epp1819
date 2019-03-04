"""
Analysis.

"""

import numpy as np
import json
import pickle
import itertools

from bld.project_paths import project_paths_join as ppj


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

def prior_samples(cov_12, prior):
    """Draw fac1 and fac2 from joint prior distribution and return the random 
    sample of fac1 and fac2.
    
    """
    mean = [0, 0]
    var3=prior[2]["var_p"]
    f12_0 = np.random.multivariate_normal(mean, cov_12, fixed["n_particles"])
    f3_0  = np.random.normal(0, var3, fixed["n_particles"])
    
    tup1 = list(itertools.product(f12_0, f3_0))

    prior=[]
    for tup in tup1:
        prior.append(np.append(tup[0], tup[1]))

    return prior
    

if __name__ == "__main__":
    prior = json.load(open(ppj("IN_MODEL_SPECS", "true_prior.json"), encoding="utf-8"))
    fixed = json.load(open(ppj("IN_MODEL_SPECS", "smoother.json"), encoding="utf-8"))
                
    np.random.seed(fixed["rnd_seed"])
    
    #Load true variances and form covarince matrix     
    cov_12 = cov_matrix(prior)
    #Draw random samples of fac1&fac2 and fac3. Merge those to form whole sample.
    prior_all = prior_samples(cov_12, prior)
    #Store the drawn samples.
    with open(ppj("OUT_ANALYSIS", "samples_from_prior.pickle"), "wb") as out_file:
        pickle.dump(prior_all, out_file)



