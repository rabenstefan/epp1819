"""Make a boxplot of the differences between estimated and true factors. For
each factor type and each period, one boxplot (over all observations) is
created (note that for the constant factor 3, only one period exists). The
boxplots visualize the median and the spread of the estimation biases.

"""

import pandas as pd
import seaborn as sns
import sys

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
