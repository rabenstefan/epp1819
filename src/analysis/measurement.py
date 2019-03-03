"""Measurement class: organizes measurements and parameters per factor."""

import numpy as np
import pandas as pd

class Measurement:
    """Organize measurement-data and parameters pertaining to the measurement
    equations of one factor. Provide probabilities of factors, given that.
    
    **Instance variables:**
        + parameters (list of dictionaries):    Each dictionary contains
                                                parameters of one measurement
                                                equation.
        + data (pd.DataFrame):  Has measurements for all measurement equations
                                and additional controls, over all observations.
    **Public methods:**
        + probability
    
    """
    
    def __init__(self, parameters, data):
        """Store parameters and measurement data for use in linear measurement
        equation.
        
        **Args:**
            + parameters (list of dictionaries):
                Each dictionary contains names 'beta1', 'beta2' (coefficients
                of controls), 'z' (coefficient of factor) and 'var' (variance
                of error). Each dictionary describes one measurement equation.
            + data (pd.DataFrame):
                Has MultiIndex (caseid, period) and columns 'control',
                'control_2', 'meas1', 'meas2', 'meas3'.
        
        **Created class attributes:**
            + meas_res (pd.DataFrame): Reduced version of data, where control-
                columns are dropped as it stores the residuals of measurements
                given controls (times coefficients).
            + fac_coff (list of scalars): Stores coefficient of factor for
                each measurement equation.
            + variances (list of scalars): Stores error variances for each
                measurement equation.
        """
        
        self.meas_res = []
        #Generate residuals of measurements given controls.
        controls = np.array(data.loc[:,['control', 'control_2']])
        for i, param_dic in enumerate(parameters):
            eq_nr = str(i+1)
            betas = np.array([param_dic['beta1'], param_dic['beta2']])
            meas = np.array(data['meas'+eq_nr])
            resid = meas - np.matmul(controls, betas)
            self.meas_res.append(pd.DataFrame(
                                                    data = resid,
                                                    index = data.index,
                                                    columns = ['res'+eq_nr]
                                                ))
        
        #Store coefficients and variances in lists.
        self.fac_coff = []
        self.variances = []
        for param_dic in parameters:
            self.fac_coff.append(param_dic['z'])
            self.variances.append(param_dic['var'])