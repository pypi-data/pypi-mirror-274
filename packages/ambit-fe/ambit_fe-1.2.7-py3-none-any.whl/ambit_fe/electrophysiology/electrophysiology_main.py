#!/usr/bin/env python3

# Copyright (c) 2019-2024, Dr.-Ing. Marc Hirschvogel
# All rights reserved.

# This source code is licensed under the MIT-style license found in the
# LICENSE file in the root directory of this source tree.

import time, sys, os
import numpy as np
from dolfinx import fem, mesh
import dolfinx.fem.petsc
import ufl
from petsc4py import PETSc

from . import electrophysiology_constitutive
from . import electrophysiology_variationalform
from .. import timeintegration
from .. import utilities
from .. import boundaryconditions
from .. import ioparams
from ..solver import solver_nonlin
from ..solver.projection import project

from ..base import problem_base, solver_base

"""
Electrophysiology
"""

class ElectrophysiologyProblem(problem_base):

    def __init__(self, io_params, time_params, fem_params, constitutive_models, bc_dict, time_curves, ioe, mor_params={}, comm=None, solidvar={}):
        super().__init__(io_params, time_params, comm=comm)

        ioparams.check_params_fem_electrophysiology(fem_params)
        ioparams.check_params_time_electrophysiology(time_params)

        self.problem_physics = 'electrophysiology'

        self.results_to_write = io_params['results_to_write']

        self.io = ioe

        # number of distinct domains (each one has to be assigned a own material model)
        self.num_domains = len(constitutive_models)
        self.domain_ids = np.arange(1,self.num_domains+1)

        self.constitutive_models = utilities.mat_params_to_dolfinx_constant(constitutive_models, self.io.mesh)

        self.order_phi = fem_params['order_phi']

        self.localsolve = False
        self.sub_solve = False

        self.dim = self.io.mesh.geometry.dim

        # type of discontinuous function spaces
        if str(self.io.mesh.ufl_cell()) == 'tetrahedron' or str(self.io.mesh.ufl_cell()) == 'triangle' or str(self.io.mesh.ufl_cell()) == 'triangle3D':
            dg_type = "DG"
            if self.order_phi > 1 and self.quad_degree < 3:
                raise ValueError("Use at least a quadrature degree of 3 or more for higher-order meshes!")
        elif str(self.io.mesh.ufl_cell()) == 'hexahedron' or str(self.io.mesh.ufl_cell()) == 'quadrilateral' or str(self.io.mesh.ufl_cell()) == 'quadrilateral3D':
            dg_type = "DQ"
            if self.order_phi > 1 and self.quad_degree < 5:
                raise ValueError("Use at least a quadrature degree of 5 or more for higher-order meshes!")
        else:
            raise NameError("Unknown cell/element type!")

        self.Vex = self.io.mesh.ufl_domain().ufl_coordinate_element()

        # model order reduction
        self.mor_params = mor_params
        if bool(self.mor_params): self.have_rom = True
        else: self.have_rom = False

        # solid problem variables
        self.solidvar = {}#alevar
        self.solidvar['F'], self.solidvar['F_old'], self.solidvar['F_mid'] = None, None, None

        # create finite element object for phi
        P_phi = ufl.FiniteElement("CG", self.io.mesh.ufl_cell(), self.order_phi)
        # function space for v
        self.V_phi = fem.FunctionSpace(self.io.mesh, P_phi)

        # continuous tensor and scalar function spaces of order order_phi
        self.V_tensor = fem.TensorFunctionSpace(self.io.mesh, ("CG", self.order_phi))
        self.V_scalar = fem.FunctionSpace(self.io.mesh, ("CG", self.order_phi))

        # a discontinuous tensor, vector, and scalar function space
        self.Vd_tensor = fem.TensorFunctionSpace(self.io.mesh, (dg_type, self.order_phi-1))
        self.Vd_vector = fem.VectorFunctionSpace(self.io.mesh, (dg_type, self.order_phi-1))
        self.Vd_scalar = fem.FunctionSpace(self.io.mesh, (dg_type, self.order_phi-1))

        # for output writing - function spaces on the degree of the mesh
        self.mesh_degree = self.io.mesh._ufl_domain._ufl_coordinate_element.degree()
        self.V_out_scalar = fem.FunctionSpace(self.io.mesh, ("CG", self.mesh_degree))
        self.V_out_vector = fem.VectorFunctionSpace(self.io.mesh, ("CG", self.mesh_degree))
        self.V_out_tensor = fem.TensorFunctionSpace(self.io.mesh, ("CG", self.mesh_degree))

        # coordinate element function space - based on input mesh
        self.Vcoord = fem.FunctionSpace(self.io.mesh, self.Vex)

        # functions
        self.dphi    = ufl.TrialFunction(self.V_phi)            # Incremental potential
        self.var_phi = ufl.TestFunction(self.V_phi)             # Test function
        self.phi     = fem.Function(self.V_phi, name="Potential")

        # values of previous time step
        self.phi_old = fem.Function(self.V_phi)
        self.phidot_old = fem.Function(self.V_phi)

        self.numdof = self.phi.vector.getSize()

        # initialize fluid time-integration class
        self.ti = timeintegration.timeintegration_electrophysiology(time_params, self.dt, self.numstep, fem_params, time_curves=time_curves, t_init=self.t_init, dim=self.dim, comm=self.comm)

        # get time factors
        self.timefac_m, self.timefac = self.ti.timefactors()

        # initialize material/constitutive classes (one per domain)
        self.ma = []
        for n in range(self.num_domains):
            self.ma.append(electrophysiology_constitutive.constitutive(self.dim, self.constitutive_models['MAT'+str(n+1)]))

        # initialize electrophysiology variational form class
        self.vf = electrophysiology_variationalform.variationalform(self.var_phi, n0=self.io.n0)

        # initialize boundary condition class
        self.bc = boundaryconditions.boundary_cond(self.io, fem_params=fem_params, vf=self.vf, ti=self.ti)

        self.bc_dict = bc_dict

        # Dirichlet boundary conditions
        if 'dirichlet' in self.bc_dict.keys():
            self.bc.dirichlet_bcs(self.bc_dict['dirichlet'], self.V_v)

        if 'dirichlet_vol' in self.bc_dict.keys():
            self.bc.dirichlet_vol(self.bc_dict['dirichlet_vol'], self.V_v)

        self.set_variational_forms()

        self.pbrom = self # self-pointer needed for ROM solver access
        self.V_rom = self.V_phi
        self.print_enhanced_info = self.io.print_enhanced_info

        # number of fields involved
        self.nfields = 1

        # residual and matrix lists
        self.r_list, self.r_list_rom = [None]*self.nfields, [None]*self.nfields
        self.K_list, self.K_list_rom = [[None]*self.nfields for _ in range(self.nfields)],  [[None]*self.nfields for _ in range(self.nfields)]


    def get_problem_var_list(self):

        is_ghosted = [1]
        return [self.phi.vector], is_ghosted


    # the main function that defines the fluid mechanics problem in terms of symbolic residual and jacobian forms
    def set_variational_forms(self):

        # set form for time derivative of phi
        self.phidot = self.ti.set_phidot(self.phi, self.phi_old, self.phidot_old)

        # set mid-point representation
        self.phidot_mid = self.timefac_m * self.phidot + (1.-self.timefac_m) * self.phidot_old
        self.phi_mid    = self.timefac   * self.phi    + (1.-self.timefac)   * self.phi_old

        # weak forms of time derivative of potential,
        self.wf_phidot, self.wf_phidot_old, self.wf_phidot_mid = ufl.as_ufl(0), ufl.as_ufl(0), ufl.as_ufl(0)
        self.wf_eflux, self.wf_eflux_old, self.wf_eflux_mid = ufl.as_ufl(0), ufl.as_ufl(0), ufl.as_ufl(0)
        self.wf_ext, self.wf_ext_old, self.wf_ext_mid = ufl.as_ufl(0), ufl.as_ufl(0), ufl.as_ufl(0)

        for n, M in enumerate(self.domain_ids):

            self.wf_phidot     += self.vf.wf_phidot(self.phidot, self.io.dx(M), F=self.solidvar['F'])
            self.wf_phidot_old += self.vf.wf_phidot(self.phidot_old, self.io.dx(M), F=self.solidvar['F'])
            self.wf_phidot_mid += self.vf.wf_phidot(self.phidot_mid, self.io.dx(M), F=self.solidvar['F'])

            self.wf_eflux     += self.vf.wf_phidot(self.ma[n].Qe(self.phi, F=self.solidvar['F']), self.io.dx(M), F=self.solidvar['F'])
            self.wf_eflux_old += self.vf.wf_phidot(self.ma[n].Qe(self.phi_old, F=self.solidvar['F_old']), self.io.dx(M), F=self.solidvar['F_old'])
            self.wf_eflux_mid += self.vf.wf_phidot(self.ma[n].Qe(self.phi_mid, F=self.solidvar['F_mid']), self.io.dx(M), F=self.solidvar['F_mid'])

        # external virtual power (from Neumann or Robin boundary conditions, body forces, ...)
        w_neumann = ufl.as_ufl(0)
        w_neumann_old = ufl.as_ufl(0)
        w_neumann_mid = ufl.as_ufl(0)
        if 'neumann' in self.bc_dict.keys():
            w_neumann     = self.bc.neumann_bcs(self.bc_dict['neumann'], self.V_v, self.Vd_scalar, self.io.bmeasures, F=self.solidvar['Fale'], funcs_to_update=self.ti.funcs_to_update, funcs_to_update_vec=self.ti.funcs_to_update_vec)
            w_neumann_old = self.bc.neumann_bcs(self.bc_dict['neumann'], self.V_v, self.Vd_scalar, self.io.bmeasures, F=self.solidvar['Fale_old'], funcs_to_update=self.ti.funcs_to_update_old, funcs_to_update_vec=self.ti.funcs_to_update_vec_old)
            w_neumann_mid = self.bc.neumann_bcs(self.bc_dict['neumann'], self.V_v, self.Vd_scalar, self.io.bmeasures, F=self.solidvar['Fale_mid'], funcs_to_update=self.ti.funcs_to_update_mid, funcs_to_update_vec=self.ti.funcs_to_update_vec_mid)
        if 'source' in self.bc_dict.keys():
            w_source      = self.bc.bodyforce(self.bc_dict['bodyforce'], self.V_v, self.Vd_scalar, self.io.dx, F=self.solidvar['Fale'], funcs_to_update=self.ti.funcs_to_update)
            w_source_old  = self.bc.bodyforce(self.bc_dict['bodyforce'], self.V_v, self.Vd_scalar, self.io.dx, F=self.solidvar['Fale_old'], funcs_to_update=self.ti.funcs_to_update_old)
            w_source_mid  = self.bc.bodyforce(self.bc_dict['bodyforce'], self.V_v, self.Vd_scalar, self.io.dx, F=self.solidvar['Fale_mid'], funcs_to_update=self.ti.funcs_to_update_mid)

        self.wf_ext     = w_neumann
        self.wf_ext_old = w_neumann_old
        self.wf_ext_mid = w_neumann_mid

        ### full weakforms

        # evaluate nonlinear terms trapezoidal-like: a * f(u_{n+1}) + (1-a) * f(u_{n})
        if self.ti.eval_nonlin_terms=='trapezoidal':

            self.weakform_phi = self.timefac_m * self.wf_phidot + (1.-self.timefac_m) * self.wf_phidot_old + \
                                self.timefac   * self.wf_eflux + (1.-self.timefac)    * self.wf_eflux_old - \
                                self.timefac   * self.wf_source - (1.-self.timefac)   * self.wf_source_old
        # evaluate nonlinear terms midpoint-like: f(a*u_{n+1} + (1-a)*u_{n})
        elif self.ti.eval_nonlin_terms=='midpoint':

            self.weakform_phi = self.wf_phidot_mid + self.wf_eflux_mid - self.wf_source_mid

        else:
            raise ValueError("Unknown eval_nonlin_terms option. Choose 'trapezoidal' or 'midpoint'.")

        self.weakform_lin_phiphi = ufl.derivative(self.weakform_phi, self.phi, self.dphi)


    # rate equations
    def evaluate_rate_equations(self, t_abs, t_off=0):

        pass


    def set_problem_residual_jacobian_forms(self):

        ts = time.time()
        utilities.print_status("FEM form compilation for electrophysiology...", self.comm, e=" ")

        self.res_phi = fem.form(self.weakform_phi)
        self.jac_phiphi = fem.form(self.weakform_lin_phiphi)

        te = time.time() - ts
        utilities.print_status("t = %.4f s" % (te), self.comm)


    def set_problem_vector_matrix_structures(self, rom=None):

        self.r_phi = fem.petsc.create_vector(self.res_phi)
        self.K_phiphi = fem.petsc.create_matrix(self.jac_phiphi)


    def assemble_residual(self, t, subsolver=None):

        # assemble velocity rhs vector
        with self.r_phi.localForm() as r_local: r_local.set(0.0)
        fem.petsc.assemble_vector(self.r_phi, self.res_phi)
        fem.apply_lifting(self.r_phi, [self.jac_phiphi], [self.bc.dbcs], x0=[self.phi.vector], scale=-1.0)
        self.r_phi.ghostUpdate(addv=PETSc.InsertMode.ADD, mode=PETSc.ScatterMode.REVERSE)
        fem.set_bc(self.r_phi, self.bc.dbcs, x0=self.phi.vector, scale=-1.0)

        self.r_list[0] = self.r_phi


    def assemble_stiffness(self, t, subsolver=None):

        # assemble system matrix
        self.K_phiphi.zeroEntries()
        fem.petsc.assemble_matrix(self.K_phiphi, self.jac_phiphi, self.bc.dbcs)
        self.K_phiphi.assemble()

        self.K_list[0][0] = self.K_phiphi


    ### now the base routines for this problem

    def read_restart(self, sname, N):

        # read restart information
        if self.restart_step > 0:
            self.io.readcheckpoint(self, N)
            self.simname += '_r'+str(N)


    def evaluate_initial(self):

        pass


    def write_output_ini(self):

        self.io.write_output(self, writemesh=True)


    def write_output_pre(self):

        pass


    def get_time_offset(self):
        return 0.


    def evaluate_pre_solve(self, t, N, dt):

        # set time-dependent functions
        self.ti.set_time_funcs(t, dt)

        # evaluate rate equations
        self.evaluate_rate_equations(t)

        # DBC from files
        if self.bc.have_dirichlet_file:
            for m in self.ti.funcs_data:
                file = list(m.values())[0].replace('*',str(N))
                func = list(m.keys())[0]
                self.io.readfunction(func, file)
                sc = m['scale']
                if sc != 1.0: func.vector.scale(sc)


    def evaluate_post_solve(self, t, N):

        pass


    def set_output_state(self, t):
        pass


    def write_output(self, N, t, mesh=False):

        self.io.write_output(self, N=N, t=t)


    def update(self):

        # update - velocity, acceleration, pressure, all internal variables, all time functions
        self.ti.update_timestep(self.phi, self.phi_old)


    def print_to_screen(self):
        pass


    def induce_state_change(self):
        pass


    def write_restart(self, sname, N):

        self.io.write_restart(self, N)


    def check_abort(self, t):
        pass


    def destroy(self):

        self.io.close_output_files(self)



class ElectrophysiologySolver(solver_base):

    def initialize_nonlinear_solver(self):

        self.pb.set_problem_residual_jacobian_forms()
        self.pb.set_problem_vector_matrix_structures()

        self.evaluate_assemble_system_initial()

        # initialize nonlinear solver class
        self.solnln = solver_nonlin.solver_nonlinear([self.pb], self.solver_params)


    def solve_initial_state(self):

        pass


    def solve_nonlinear_problem(self, t):

        self.solnln.newton(t)


    def print_timestep_info(self, N, t, ni, li, wt):

        # print time step info to screen
        self.pb.ti.print_timestep(N, t, self.solnln.lsp, ni=ni, li=li, wt=wt)
