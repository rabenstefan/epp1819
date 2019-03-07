"""Plot differences between estimated and true factors."""

import pandas as pd
import seaborn as sns
import sys

# =============================================================================
# import os
# os.getcwd()
# sys.path.insert(0,'./../../bld/')
# from project_paths import project_paths_join as ppj
# =============================================================================

from bld.project_paths import project_paths_join as ppj

def plot_differences(estimates, truth, spec):
    diff = estimates - truth
    ax = sns.boxplot(x = diff.loc[(slice(None),1),'fac3'])
    fig = ax.get_figure()
    fig.savefig(ppj("OUT_FIGURES", spec+"_boxplot_fac3.png"))
    fig.clear()
    
    unstacked_f1 = diff.loc[:,'fac1'].unstack(level=1)
    bp_fac1 = sns.boxplot(data = unstacked_f1)
    fig = bp_fac1.get_figure()
    fig.savefig(ppj("OUT_FIGURES", spec+"_boxplot_fac1.png"))
    fig.clear()
    
    unstacked_f2 = diff.loc[:,'fac2'].unstack(level=1)
    bp_fac2 = sns.boxplot(data = unstacked_f2)
    fig = bp_fac2.get_figure()
    fig.savefig(ppj("OUT_FIGURES", spec+"_boxplot_fac2.png"))
    
    
if __name__ == '__main__':
    spec = sys.argv[1]
    truth = pd.read_pickle(ppj('OUT_ANALYSIS','true_facs.pkl'))
    est = pd.read_pickle(ppj('OUT_ANALYSIS',spec+'_factor_estimates.pkl'))
    plot_differences(est, truth, spec)
