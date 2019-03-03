"""Structure measurements per factor and save as pickle."""

import numpy as np
import pandas as pd
"""
import sys, os
os.getcwd()
sys.path.insert(0,'./../../bld/')
from project_paths import project_paths_join as ppj
"""
from bld.project_paths import project_paths_join as ppj

def prepare_data():
    """Merge tables generated from simulated data, where columns 'fac1',
    'fac2', 'fac3' from **table_2** contain the factor ids in **table_1**
    and columns 'x1', 'x2' from **table_2** contain control ids in **table_3**.
    
    The output are one pandas dataframe (saved as pickle) per factor, named
    'meas_facX' (X as 1, 2, 3), that contains the multiindex (caseid, period),
    the two controls, and three measurements.
    
    """

    # Read in dataframes from Stata files.
    factor = pd.read_stata(
                            ppj("OUT_DATA","tables", "data_table_1.dta"),
                            index_col = 'factor_id',
                            columns = ['factor_id', 'meas1', 'meas2', 'meas3']
                          )
    case = pd.read_stata(
                            ppj("OUT_DATA", "tables", "data_table_2.dta")
                        )
    case.set_index(['caseid', 't'], inplace = True)
    control = pd.read_stata(
                                ppj("OUT_DATA", "tables", "data_table_3.dta"),
                                index_col = 'cont_id'
                            )
    
    # Join data at indices, generate one dataframe per factor
    # and save as pickle.
    c_nr = ['x1', 'x2']
    for nr, c in enumerate(c_nr):
        case = case.join(control, on = c, rsuffix = '_'+str(nr+1))
    case.drop(c_nr, axis = 1, inplace = True)
    
    f_nr=['fac1', 'fac2', 'fac3']
    dataframes = []
    
    for nr, f in enumerate(f_nr):
        dataframes.append(case.join(factor, on = f))
        dataframes[nr].drop(f_nr, axis = 1, inplace = True)
        dataframes[nr].drop_duplicates(inplace = True)
        dataframes[nr].to_pickle(ppj("OUT_ANALYSIS", 'meas_'+f+'.pkl'))
    
if '__main__' == __name__:
    prepare_data()





