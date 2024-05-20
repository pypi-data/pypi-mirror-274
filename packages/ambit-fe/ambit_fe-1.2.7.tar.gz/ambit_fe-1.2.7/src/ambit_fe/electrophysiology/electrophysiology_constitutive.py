#!/usr/bin/env python3

# Copyright (c) 2019-2024, Dr.-Ing. Marc Hirschvogel
# All rights reserved.

# This source code is licensed under the MIT-style license found in the
# LICENSE file in the root directory of this source tree.

import ufl
from petsc4py import PETSc

#from .electrophysiology_material import materiallaw

"""
Electrophysiology constitutive class
"""

class constitutive:

    def __init__(self, dim, materials):

        self.dim = dim

        self.matmodels = []
        for i in range(len(materials.keys())):
            self.matmodels.append(list(materials.keys())[i])

        self.matparams = []
        for i in range(len(materials.values())):
            self.matparams.append(list(materials.values())[i])

        # identity tensor
        self.I = ufl.Identity(self.dim)


    # Electrical flux Qe
    def Qe(self, phi_, F=None):

        if F is not None:
            grad_phi_ = ufl.grad(phi_)*ufl.inv(F)
        else:
            grad_phi_ = ufl.grad(phi_)

        eflux = ufl.constantvalue.zero(self.dim)

        #mat = materiallaw(grad_phi_,self.I)

        m = 0
        for matlaw in self.matmodels:

            # extract associated material parameters
            matparams_m = self.matparams[m]

            if matlaw == 'newtonian':

                eflux += 1.0*grad_phi_#mat.newtonian(matparams_m)

            else:

                raise NameError("Unknown electrophysiology material law!")

            m += 1

        return eflux
