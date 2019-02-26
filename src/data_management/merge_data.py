"""Merge tables generated from simulated data.

"""
import numpy as np
import pandas as pd
import os
os.chdir('C:\\Users\\ASUS\\Desktop\\isler\\Bonn\\Winter_2018\\EPP\\epp_project\\epp_stata\\epp_final_project\\bld\\out\\data')
#from bld.project_paths import project_paths_join as ppj


factor = pd.read_stata('data_table_1.dta')
case = pd.read_stata('data_table_2.dta')
control = pd.read_stata('data_table_3.dta')

