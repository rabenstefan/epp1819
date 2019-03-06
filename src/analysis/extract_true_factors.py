"""Organize true factors in DataFrame with MultiIndex and save as pickle."""

import numpy as np
import pandas as pd

# =============================================================================
# import sys, os
# os.getcwd()
# sys.path.insert(0,'./../../bld/')
# from project_paths import project_paths_join as ppj
# =============================================================================

from bld.project_paths import project_paths_join as ppj

def extract_true_factors():
    """Merge tables generated from simulated data, where columns 'fac1',
    'fac2', 'fac3' from **table_2** contain the factor ids in **table_1**.
    
    The output is one pandas dataframe (saved as pickle) that contains the
    multiindex (caseid, period) and the three (true) factors.
    
    """

    # Read in dataframes from Stata files.
    factor = pd.read_stata(
                            ppj("OUT_DATA","tables", "data_table_1.dta"),
                            index_col = 'factor_id',
                            columns = ['factor_id', 'true_fac']
                          )
    f_nr=['fac1', 'fac2', 'fac3']
    case = pd.read_stata(
                            ppj("OUT_DATA", "tables", "data_table_2.dta"),
                            columns = f_nr + ['caseid', 't']
                        )
    case.set_index(['caseid', 't'], inplace = True)
    
    # Join data at indices, generate one dataframe and save as pickle.
    
    for f in f_nr:
        case = case.join(factor, on = f, rsuffix='_'+f)
        
    case.drop(f_nr, axis = 1, inplace = True)
    case.columns = f_nr

    case.to_pickle(ppj("OUT_ANALYSIS", 'true_facs.pkl'))
    
if '__main__' == __name__:
    extract_true_factors()




