"""
Dummy test script for the dummy template module.

.. module:: pymin.tests.test_arith
   :synopsis: test the dummy template module

.. moduleauthor:: Bryant Finney <bryant@outdoorlinkinc.com>
   :github: https://github.com/bryant-finney
"""

from pymint.arith import add


def test_add():
    """Make sure it can add."""
    assert add(2, 2) == 4
    assert add(-2, 7) == 5
