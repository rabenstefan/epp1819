"""Merge tables generated from simulated data.

"""
import numpy as np
import pandas as pd
import pickle
# =============================================================================
# import os
# os.chdir('C:\\Users\\ASUS\\Desktop\\isler\\Bonn\\Winter_2018\\EPP\\epp_project\\epp_stata\\epp_final_project\\bld\\out\\data')
# =============================================================================
from bld.project_paths import project_paths_join as ppj


factor = pd.read_stata(ppj("OUT_DATA","tables", "data_table_1.dta"))
case = pd.read_stata(ppj("OUT_DATA", "tables",  "data_table_2.dta"))
control = pd.read_stata(ppj("OUT_DATA","tables",  "data_table_3.dta"))

case_controls = pd.merge(
        case.reset_index(),
        control.reset_index(),
        on=['caseid']
)


f_nr=['fac1', 'fac2', 'fac3']
df=['d1', 'd2', 'd3']

for f in range(len(f_nr)):
    df[f]=pd.merge(
        left=factor, right=case_controls, how='inner', 
        left_on='factor_id', right_on=f_nr[f]
    )
    
data = df[0].append([df[1], df[2]])
data_all = data.to_csv(ppj("OUT_DATA", "data_all.dta"))
# =============================================================================
# data_all = data.to_csv("data_all.csv"), sep=",")
# def save_data(sample):
#     sample.tofile(ppj("OUT_DATA", "data_all.csv"), sep=",")
# 
# 
# if __name__ == "__main__":
#     sample = data_all
#     save_data(sample)
# =============================================================================





