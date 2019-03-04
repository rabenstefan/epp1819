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
from transition import Transition


if __name__ == "__main__":
    trans_params = json.load(
                             open(
                                     ppj("IN_MODEL_SPECS", "transitions.json"),
                                     encoding = "utf-8"
                                 )
                            )
    trans_obj = Transition(trans_params, [1, 1, 0])
    test_state = np.array([[[1, 7],[2, 5]],[[3, 8],[1, 3]],[[5, 9],[4, 2]]])
    test_errors = np.array([[[.5, .3],[-.1, .8]],[[-.3, -.2],[.1, -.5]]])
    test_next = trans_obj.next_state(test_state, test_errors)
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
    test_facs = pd.DataFrame(
                                data = np.ones((4000,100)),
                                columns = ['fac'+str(i+1) for i in range(100)]
                            )
    probs = meas_objs[0].marginal_probability(test_facs, 1)

