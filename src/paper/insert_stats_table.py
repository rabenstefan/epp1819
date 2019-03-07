"""Insert table with summary statistics in the latex file."""

PLACEHOLDER = '$table1'

import pandas as pd
import numpy as np

# =============================================================================
# import os, sys
# os.getcwd()
# sys.path.insert(0,'./../../bld/')
# from project_paths import project_paths_join as ppj
# =============================================================================
from bld.project_paths import project_paths_join as ppj

def table_to_latex(tables):
    dfs = []
    for i, tab in enumerate(tables):
        nr_p, nr_f = tab['bias'].shape
        dfs.append(pd.DataFrame(
                    index = range(1,nr_p+1),
                    columns = pd.MultiIndex.from_product(
                                                        [range(1,nr_f+1),
                                                         ['Avg bias', 'RMSE']],
                                                         names = ['Factor',
                                                                  'Statistic']
                                                         ),
                    data = np.zeros((nr_p, nr_f*2))
                                ))
        dfs[i].loc[:, (slice(None), 'Avg bias')] = tab['bias'].values
        dfs[i].loc[:, (slice(None), 'RMSE')] = tab['rmse'].values
        
    latex_tables = "\\begin{center} "
    for df in dfs:
        latex_tables += df.to_latex()+" \\end{center} \\begin{center} "
    return latex_tables+" \\end{center}"


if __name__ == '__main__':
    tables = []
    f_nr = ['fac1', 'fac2', 'fac3']
    for spec in 'rnd_prior','deg_prior':
        bias = pd.read_csv(
                            ppj('OUT_TABLES','{}_est_bias.csv'.format(spec)),
                            usecols = f_nr
                          )
        rmse = pd.read_csv(
                            ppj('OUT_TABLES','{}_est_rmse.csv'.format(spec)),
                            usecols = f_nr
                          )
        tables.append({'bias': bias, 'rmse': rmse})
    latex_code = table_to_latex(tables)
    buffer = []
    with open(ppj('PROJECT_ROOT','src/paper/research_paper.tex')) as f:
        for line in f:
            buffer.append(line.replace(PLACEHOLDER, latex_code))
    with open(ppj('OUT_PAPER','research_paper.tex'),'w') as f:
        f.writelines(buffer)