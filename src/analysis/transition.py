"""Transition class: provide transition equations and -probabilities.
TransitionFactorSettingError class: exception for unfit factor settings.
TransitionFactorValuesError class: exception for wrong factor values.
"""

import numpy as np
from scipy.stats import norm

class Transition:
    """
    Instance variables:
        + parameters (list of dictionaries)
        + factor_setting (list of binaries)
        
    Public methods:
        + next_state
        + marginal_probability
    """
    
    def __init__(self, parameters, factor_setting):
        """Store parameters for the (nonlinear) transition equations and
        the setting of transitions for the factor types.
        
        Args:
            + *parameters* (list of dictionaries): Each dictionary contains
                names 'phi', 'lambda', 'gammaX' (X in 1, 2, 3), and 'var_u'
                (for variance of additive error). Each dictionary describes
                one transition equation.
            + *factor_setting* (list of binaries (0 or 1)): Each binary
                describes the transition of one factor type, where '1' stands 
                for the transition equation in *parameters* whose list-position
                is equal to the position of the binary, and '0' stands for a
                constant factor type (no transition).
                Is expected to **be of length 3**.
        
        Created class attributes:
            + *params* (list of dictionaries)
            + *factor_setting* (list of binaries (0 or 1))
        """
        
        self.params = parameters
        self.sds = [np.sqrt(p['var_u']) for p in parameters]
        self.factor_setting = factor_setting
        
    def _transition_equation(self, nr, factors):
        """Calculate (expected) next state of one factor, given inputs.
        
        Args:
            + *nr* (integer): Factor number to which transition equation
                belongs (**starts at 0**).
            + *factors* (np.ndarray): Array of arbitrary shape, but with
                **first dimension of length 3** (is taken as the three inputs).
        
        Returns:
            + expected next state of factor type *nr* (np.ndarray): Array with
                same shape as *factors*, but first dimension is 'flat'
        """
        
        # Define CES-function with parameters from factor type *nr*.
        ces = lambda a1, a2, a3 : np.log(
                                            self.params[nr]['gamma1']*
                                            np.exp(
                                                    self.params[nr]['phi']*
                                                    self.params[nr]['lambda']*
                                                    np.log(a1)
                                                  )
                                            + self.params[nr]['gamma2']*
                                            np.exp(
                                                    self.params[nr]['phi']*
                                                    np.log(a2)
                                                  )
                                            + self.params[nr]['gamma3']*
                                            np.exp(
                                                    self.params[nr]['phi']*
                                                    np.log(a3)
                                                  )
                                        ) / (
                                                self.params[nr]['phi']*
                                                self.params[nr]['lambda']
                                            )
        return ces(factors[0, ...], factors[1, ...], factors[2, ...])
    
    def _density(self, nr, x):
        """Return value of density evaluated at x.
        
        Args:
            + *nr* (integer): Factor number (**starts at 0**).
            + *x* (np.ndarray): matrix of values
        
        Returns:
            + np.ndarray of normal densities at x
        """
        
        return norm.pdf(x, scale = self.sds[nr])
        
    def next_state(self, state, errors):
        """Calculate next state of all factors, given last state and normalized
        errors.
        
        Args:
            + *state* (np.ndarray): Array of arbitrary shape, but with
                **first dimension of length 3** (is taken as the three factor
                types). Contains state for one period over all observations and
                particles.
            + *errors* (np.ndarray): Array of **same shape as *state* **, but
                first dimension only as long as number of non-constant factors.
                Contains additive, normalized errors to transition equations.
                They are attributed to factor types along first dimension, 
                sorted from first to last non-constant factor type.
        
        Returns:
            + next state of factors (np.ndarray): Has same shape as *state*.
        """
    
        if (
                sum(self.factor_setting) != errors.shape[0] or
                len(self.factor_setting) != state.shape[0]
            ):
            raise TransitionFactorSettingError
        if np.amin(state) <= 0:
            raise TransitionFactorValuesError
            
        next_state = np.zeros(state.shape)
        sum_trans = 0
        for nr, trans in enumerate(self.factor_setting):
            # Take same values if factor type is constant.
            if 0 == trans:
                next_state[nr, ...] = state[nr, ...]
            else:
                next_state[nr, ...] = (
                                        self._transition_equation(
                                                                   nr, 
                                                                   state
                                                                 )
                                        + self.sds[nr]*errors[sum_trans, ...]
                                     )
                sum_trans += 1
        return next_state
    
    def marginal_probability(self, next_state, state):
        """Calculate (marginal) probabilities of factors in *state*, given
        transition equations and *next_state*. The probabilities from each
        transition equation are multiplied among non-constant factor types
        (due to the independence of additive errors). For constant factor
        types, factors in *state* that do not fit to *next_state* get assigned
        probability 0.
        
        Args:
            + *next_state* (np.ndarray): Array of shape 3xN, where N is the
                number of observations. Contains the next state of all three
                factor types, for all observations.
            + *state* (np.ndarray): Array of shape 3xNxM, where M is the number
                of factors per observation and type. The three factor types are
                the input to the transition equations.
        
        Returns:
            + marginal probabilities (np.ndarray): Array of shape NxM, that
                contains the marginal probabilities that the three-factor-
                combinations in *state* can produce *next_state*.
        """
        
        ret_arr = np.zeros(state.shape[1:])
        # Start with constant factor types to identify fitting indices.
        const = np.nonzero(0 == np.array(self.factor_setting))[0]
        are_equal = np.ones(state.shape[1:])
        for c_i in const:
            is_equal = lambda x : next_state[c_i, :] == x
            are_equal *= np.apply_along_axis(is_equal, 0, state[c_i, ...])
        fit_indices = np.nonzero(are_equal)
        fit_factors = state[:, fit_indices[0], fit_indices[1]]
        # Calculate marg. probabilities for fitting indices.
        nonconst = np.nonzero(self.factor_setting)[0]
        ret_arr[fit_indices[0], fit_indices[1]] = 1
        for nc_i in nonconst:
            marg_prob = self._density(
                                      nc_i,
                                      next_state[nc_i, fit_indices[0]] -
                                      self._transition_equation(
                                                                nc_i,
                                                                fit_factors
                                                               )
                                     )
            ret_arr[fit_indices[0], fit_indices[1]] *= marg_prob
        return ret_arr
        
class TransitionFactorSettingError(Exception):
    
    def __str__(self):
        return "Input does not fit to number of non-constant factor types."

class TransitionFactorValuesError(Exception):
    
    def __str__(self):
        return "Input contains non-positive factor values."