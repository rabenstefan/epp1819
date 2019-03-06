"""Measurement class: organizes measurements and parameters per factor.
MeasurementDimensionError class: exception if dimensions do not fit.
"""

import numpy as np
import pandas as pd
from scipy.stats import norm

class Measurement:
    """Organize measurement-data and parameters pertaining to the measurement
    equations of one factor. Provide probabilities of factors, given that.
    
    Instance variables:
        + parameters (list of dictionaries):    Each dictionary contains
                                                parameters of one measurement
                                                equation.
        + data (pd.DataFrame):  Has measurements for all measurement equations
                                and additional controls, over all observations.
    Public methods:
        + marginal_probability
    
    """
    
    def __init__(self, parameters, data):
        """Store parameters and measurement data for use in linear measurement
        equation.
        
        Args:
            + *parameters* (list of dictionaries):
                Each dictionary contains names 'beta1', 'beta2' (coefficients
                of controls), 'z' (coefficient of factor) and 'var' (variance
                of error). Each dictionary describes one measurement equation.
            + *data* (pd.DataFrame):
                Has MultiIndex (caseid, period) and columns 'control',
                'control_2', 'meas1', 'meas2', 'meas3'.
        
        Created class attributes:
            + *meas_res* (list of pd.DataFrame): DataFrame with MultiIndex
                (caseid, period) and column that stores the residuals of
                measurements given controls (and coefficients), for each
                measurement equation.
            + *fac_coeff* (list of scalars): Stores coefficient of factor for
                each measurement equation.
            + *variances* (list of scalars): Stores error variances for each
                measurement equation.
        """
        
        self.meas_res = []
        self.fac_coeff = []
        self.variances = []
        controls = np.array(data.loc[:,['control', 'control_2']])
        for i, param_dic in enumerate(parameters):
            eq_nr = str(i+1)
            betas = np.array([param_dic['beta1'], param_dic['beta2']])
            meas = np.array(data['meas'+eq_nr])
            #Generate residuals of measurements given controls.
            resid = meas - np.matmul(controls, betas)
            self.meas_res.append(
                                    pd.DataFrame(
                                                    data = resid,
                                                    index = data.index,
                                                    columns = ['res'+eq_nr]
                                                )
                                 )
        
            #Store coefficients and variances in lists.
            self.fac_coeff.append(param_dic['z'])
            self.variances.append(param_dic['var'])
    
    def _density(self, x, var):
        """Return value of density evaluated at x.
        
        Args:
            + *x* (np.ndarray): matrix of values
            + *var* (scalar): variance of normal density
        
        Returns:
            + np.ndarray of normal densities at x
        """
        
        return norm.pdf(x, scale = np.sqrt(var))
    
    def marginal_probability(self, factors, period):
        """Returns marginal (since density-values are returned) probability of
        factors, given measurements, for one period.
        
        Args:
            + *factors* (np.ndarray): Array with shape NxM, where N is number
                of observations and M is number of factors per period and 
                observation.
            + *period* (integer): number of period, starting at 1
            
        Returns:
            + marginal probabilities (np.ndarray): Array with shape NxM, filled
                with density-values of the factors at the according indices.
        """
        
        nr_obs, nr_facs = factors.shape
        marginals = np.ones((nr_obs, nr_facs))
        # Calculate densities for each measurement equation.
        for i, var in enumerate(self.variances):
            meas = self.meas_res[i].xs(period, level = 1)
            if (meas.empty) or (nr_obs != meas.shape[0]):
                raise MeasurementDimensionError
            x = (
                    np.repeat(meas.values, nr_facs, axis = 1)
                        - self.fac_coeff[i]*factors
                )
            marginals *= self._density(x, var)
        
        return marginals
            
            
        
class MeasurementDimensionError(Exception):
    
    def __str__(self):
        return (
                "Measurements are not available for this number of " +
                "observations and / or periods."
               )