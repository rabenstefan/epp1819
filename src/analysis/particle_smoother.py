"""
Analysis.

"""

import numpy as np
import pandas as pd
import json

import sys, os
os.getcwd()
sys.path.insert(0,'./../../bld/')
from project_paths import project_paths_join as ppj

#from bld.project_paths import project_paths_join as ppj
from measurement import Measurement


if __name__ == "__main__":
    meas_params = json.load(
                             open(
                                    ppj("IN_MODEL_SPECS", "measurements.json"),
                                    encoding="utf-8"
                                 )
                            )
    f_nr = ['fac1', 'fac2', 'fac3']
    meas_objs = []
    for fac in f_nr:
        data = pd.read_pickle(ppj("OUT_ANALYSIS", 'meas_'+fac+'.pkl'))
        params = []
        for param_dic in meas_params:
            if fac == param_dic['factor']:
                params.append(param_dic)
        meas_objs.append(Measurement(params, data))    
    

