#!/usr/bin/env python3

# Copyright (c) 2019-2024, Dr.-Ing. Marc Hirschvogel
# All rights reserved.

# This source code is licensed under the MIT-style license found in the
# LICENSE file in the root directory of this source tree.

import ufl

"""
Electrophysiology variational forms class
"""

class variationalform():

    def __init__(self, var_phi, n0=None):
        self.var_phi = var_phi

        self.n0 = n0


    # time derivative of potential
    def wf_phidot(self, phidot, ddomain, F=None):

        return ufl.dot(phidot, self.var_phi)*ddomain


    # electrical flux
    def wf_eflux(self, eflux, ddomain, F=None):

        return ufl.inner(eflux,ufl.grad(self.var_phi)) * ddomain


    # Neumann BC
    def wf_neumann(self, func, dboundary, F=None):

        return ufl.dot(func, self.var_d)*dboundary


    # source
    def wf_source(self, func, funcdir, ddomain, F=None):

        return func*ufl.dot(funcdir, self.var_d)*ddomain
