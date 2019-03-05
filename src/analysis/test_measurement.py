import sys
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
from measurement import Measurement
from scipy.stats import norm

if __name__ == '__main__':
    status = pytest.main([sys.argv[1]])
    sys.exit(status)
    
@pytest.fixture
def setup_2obs2parts_sameparams():
    out = {}
    params = {'beta1': 1, 'beta2': 1, 'z': 1, 'var': 1/(2*np.pi)}
    meas_data = pd.DataFrame(
                                     {
                                        'control': [1, 2],
                                        'control_2': [1, 1],
                                        'meas1': [-1, 5],
                                        'meas2': [0, 5],
                                        'meas3': [-1, 6]
                                     },
                                     index = [[1, 2], [1, 1]]
                             )
    out['meas_obj'] = Measurement([params, params, params], meas_data)
    out['facs_data'] = pd.DataFrame([[-3, -2], [2, 3]])
    return out

@pytest.fixture
def expected_2obs2parts_sameparams():
    out = {}
    sd = np.sqrt(1/(2*np.pi))
    d1 = np.array([[0, 1], [0, 1]])
    d2 = np.array([[1, 0], [0, 1]])
    d3 = np.array([[0, 1], [1, 0]])
    probs = norm.pdf(d1, scale=sd)*norm.pdf(d2,scale=sd)*norm.pdf(d3,scale=sd)
    out['probs'] = pd.DataFrame(probs)
    return out

def test_marginal_probability_2obs2parts(
                                            setup_2obs2parts_sameparams,
                                            expected_2obs2parts_sameparams
                                        ):
    meas = setup_2obs2parts_sameparams['meas_obj']
    probs = meas.marginal_probability(
                                      setup_2obs2parts_sameparams['facs_data'],
                                      1
                                     )
    assert_frame_equal(
                        probs,
                        expected_2obs2parts_sameparams['probs']
                       )