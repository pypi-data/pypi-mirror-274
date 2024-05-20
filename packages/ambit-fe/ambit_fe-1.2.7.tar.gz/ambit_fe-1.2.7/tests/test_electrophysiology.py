#!/usr/bin/env python3

"""
- electrophysiology
"""

import ambit_fe

import sys
import numpy as np
from pathlib import Path
import pytest


@pytest.mark.electrophysiology
def test_main():

    basepath = str(Path(__file__).parent.absolute())

    # reads in restart step from the command line
    try: restart_step = int(sys.argv[1])
    except: restart_step = 0

    IO_PARAMS         = {'problem_type'          : 'electrophysiology',
                         'mesh_domain'           : basepath+'/input/blockhex_domain.xdmf',
                         'mesh_boundary'         : basepath+'/input/blockhex_boundary.xdmf',
                         'write_results_every'   : -1,
                         'write_restart_every'   : -1,
                         'restart_step'          : restart_step,
                         'output_path'           : basepath+'/tmp/',
                         'results_to_write'      : ['potential'],
                         'simname'               : 'electrophysiology'}

    SOLVER_PARAMS     = {'solve_type'            : 'direct',
                         'tol_res'               : 1.0e-8,
                         'tol_inc'               : 1.0e-5,
                         'maxiter'               : 25,
                         'divergence_continue'   : None}

    TIME_PARAMS       = {'maxtime'               : 0.5,
                         'dt'                    : 0.1,
                         'timint'                : 'ost',
                         'theta_ost'             : 0.5}

    FEM_PARAMS        = {'order_phi'             : 1,
                         'quad_degree'           : 5}

    MATERIALS         = {'MAT1' : {'visco_green' : {'eta' : 2.0},
                                   'inertia'     : {'rho0' : 1.0e-6}}}


    # define your load curves here (syntax: tcX refers to curve X, to be used in BC_DICT key 'curve' : [X,0,0], or 'curve' : X)
    class time_curves():

        def tc1(self, t):
            return 3.*t

    BC_DICT           = { 'neumann' : [{'id' : [3], 'dir' : 'xyz_ref', 'curve' : [0,0,1]}],
                            'robin' : [{'type' : 'spring', 'id' : [1,6], 'dir' : 'normal_ref', 'stiff' : 5.0}] }


    # problem setup
    problem = ambit_fe.ambit_main.Ambit(IO_PARAMS, TIME_PARAMS, SOLVER_PARAMS, FEM_PARAMS, MATERIALS, BC_DICT, time_curves=time_curves())

    # solve time-dependent problem
    problem.solve_problem()


    # --- results check
    tol = 1.0e-6

    check_node = []
    check_node.append(np.array([0.0, 0.0, 0.0]))

    phi_corr = np.zeros(len(check_node))

    ## correct results
    phi_corr[0] = 0

    check1 = ambit_fe.resultcheck.results_check_node(problem.mp.phi, check_node, phi_corr, problem.mp.V_phi, problem.mp.comm, tol=tol, nm='phi')
    success = ambit_fe.resultcheck.success_check([check1], problem.mp.comm)

    if not success:
        raise RuntimeError("Test failed!")



if __name__ == "__main__":

    test_main()
