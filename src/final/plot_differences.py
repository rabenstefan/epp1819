"""Plot differences between estimated and true factors."""

import pandas as pd
import seaborn as sns

from bld.project_paths import project_paths_join as ppj

def plot_differences():
    estimates = pd.read_csv(ppj('OUT_ANALYSIS','estimated_factors.csv'))
    truth = pd.read_pickle(ppj('OUT_ANALYSIS','true_facs.pkl'))
    diff = estimates - truth
    bp_fac3 = sns.boxplot(x = diff.loc[(slice(None),1),'fac3'])
    fig_fac3 = bp_fac3.get_figure()
    fig_fac3.savefig(ppj("OUT_FIGURES","boxplot_fac3.png"))
    
if __name__ == '__main__':
    plot_differences()