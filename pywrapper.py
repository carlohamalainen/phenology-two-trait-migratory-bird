"""
To use this:

    sudo pip install oct2py
"""

import os.path

import oct2py as op

def solvedbo(u_q):
    oct_session = op.Oct2Py()
    oct_session.addpath(os.path.abspath(os.path.curdir))

    oct_session.eval('[x_cV, yzV, nV, z_n] = solvedbowrapper(%f)' % u_q)

    return { 'x_cV': oct_session.pull('x_cV'),
             'yzV':  oct_session.pull('yzV'),
             'nV':   oct_session.pull('nV'),
             'z_n':  oct_session.pull('z_n'),
           }
