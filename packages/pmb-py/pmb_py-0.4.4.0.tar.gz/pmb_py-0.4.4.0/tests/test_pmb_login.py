import os
from pmb_py import log_in, log_out


def test_pmb_loggin1():
    re = log_in(os.environ['TESTUSER'], os.environ['TESTPW'])
    assert re