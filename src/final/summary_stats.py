"""Summarise estimation results with descriptive statistics and save them in
two tables. Specifically, the average bias and the root mean square error is
provided for all factor types and periods.

"""

import pandas as pd
import sys

from bld.project_paths import project_paths_join as ppj

def summary_stats(est, truth):
    diff = est - truth
    # Calculate mean bias and root mean square error per period and factor.
    biases = diff.mean(level = 1)
    rmses = diff.std(level = 1, ddof = 0)
    
    return [biases, rmses]
    
if __name__ == '__main__':
    spec = sys.argv[1]
    truth = pd.read_pickle(ppj('OUT_ANALYSIS','true_facs.pkl'))
    est = pd.read_pickle(ppj('OUT_ANALYSIS',spec+'_factor_estimates.pkl'))
    table_bias, table_rmse = summary_stats(est, truth)
    table_bias.to_csv(ppj('OUT_TABLES','{}_est_bias.csv'.format(spec)))
    table_rmse.to_csv(ppj('OUT_TABLES','{}_est_rmse.csv'.format(spec)))