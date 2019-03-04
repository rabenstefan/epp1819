"""Transition class: provide transition equations and -probabilities.
TransitionFactorSettingError class: exception for wrong inputs.
"""

import numpy as np

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
        
    def next_state(self, state, errors):
        """Calculate next state of all factors, given last state and errors.
        
        Args:
            + *state* (np.ndarray): Array of arbitrary shape, but with
                **first dimension of length 3** (is taken as the three factor
                types). Contains state for one period over all observations and
                particles.
            + *errors* (np.ndarray): Array of **same shape as *state* **, but
                first dimension only as long as number of non-constant factors.
                Contains additive errors to transition equations. They are
                attributed to factor types along first dimension, sorted from
                first non-constant to last non-constant factor type.
        
        Returns:
            + next state of factors (np.ndarray): Has same shape as *state*.
        """
    
        if (
                sum(self.factor_setting) != errors.shape[0] or
                len(self.factor_setting) != state.shape[0]
            ):
            raise TransitionFactorSettingError
            
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
                                        + errors[sum_trans, ...]
                                     )
                sum_trans += 1
        return next_state
        
class TransitionFactorSettingError(Exception):
    
    def __str__(self):
        return "Input does not fit to number of non-constant factor types."