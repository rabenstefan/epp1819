import sys
import numpy as np
from numpy.testing import assert_allclose
import pytest
from transition import Transition

if __name__ == '__main__':
    status = pytest.main([sys.argv[1]])
    sys.exit(status)
    
@pytest.fixture
def setup_1nonconst_factor_next_state():
    out = {}
    params = {
                'phi': 1, 'lambda': 1, 'gamma1': 1, 'gamma2': 0, 'gamma3': 0,
                'var_u': 0.01
             }
    out['trans_obj'] = Transition([params],[1, 0, 0])
    out['state'] = np.array(
                            [[[1, 2],[3, 4]],
                             [[1, 1],[1, 1]],
                             [[2, 2],[2, 2]]]
                           )
    out['errors'] = np.array([[[.1, .2], [.3, .4]]])
    return out

@pytest.fixture
def expected_1nonconst_factor_next_state():
    out = {}
    out['next'] = np.array([
                            [[1.01, 2.02],[3.03, 4.04]],
                            [[1, 1],[1, 1]],
                            [[2, 2],[2, 2]]
                           ])
    return out

@pytest.fixture
def setup_1nonconst_factor_marg_prob():
    out = {}
    params = {
                'phi': 1, 'lambda': 1, 'gamma1': 1, 'gamma2': 0, 'gamma3': 0,
                'var_u': 0.01
             }
    out['trans_obj'] = Transition([params], [1, 0, 0])
    out['state'] = np.array(
                            [[[1, 1], [1, 1]],
                             [[2, 3], [4, 5]],
                             [[6, 7], [8, 9]]]
                            )
    out['next_state'] = np.array(
                                    [[1.1, 0.9],
                                     [3, 4],
                                     [7, 8]]
                                )
    return out

@pytest.fixture
def expected_1nonconst_factor_marg_prob():
    out = {}
    prob = np.exp(-.5)/np.sqrt(0.02*np.pi)
    out['marg_prob'] = np.array(
                                    [[0, prob],
                                     [prob, 0]]
                                )
    return out

def test_next_state_1nonconst_factor(
                                        setup_1nonconst_factor_next_state,
                                        expected_1nonconst_factor_next_state
                                    ):
    trans = setup_1nonconst_factor_next_state['trans_obj']
    next_state = trans.next_state(
                                  setup_1nonconst_factor_next_state['state'],
                                  setup_1nonconst_factor_next_state['errors']
                                 )
    assert_allclose(
                        next_state,
                        expected_1nonconst_factor_next_state['next']
                   )
def test_marginal_probability(
                                setup_1nonconst_factor_marg_prob,
                                expected_1nonconst_factor_marg_prob
                             ):
    trans = setup_1nonconst_factor_marg_prob['trans_obj']
    marginal = trans.marginal_probability(
                                setup_1nonconst_factor_marg_prob['next_state'],
                                setup_1nonconst_factor_marg_prob['state']
                                         )
    assert_allclose(
                        marginal,
                        expected_1nonconst_factor_marg_prob['marg_prob']
                   )