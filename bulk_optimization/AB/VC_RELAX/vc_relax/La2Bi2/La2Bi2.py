#!/usr/bin/env python
#SBATCH -p iric,owners,normal 
#SBATCH --job-name=La2Bi2
#SBATCH --output=La2Bi2.out
#SBATCH --error=La2Bi2.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=$USER@stanford.edu
#SBATCH --ntasks-per-node=16

import numpy as np    #vectors, matrices, lin. alg., etc.
import matplotlib
matplotlib.use('Agg') #turn off screen output so we can plot from the cluster
from ase.utils.eos import *  # Equation of state: fit equilibrium latt. const
from ase.units import kJ
from ase.lattice import bulk
from ase import *
from espresso import espresso
from ase.optimize import BFGS
from ase.constraints import StrainFilter
from ase.db import connect

pw=800.
dw=8000.
xc='BEEF-vdW'
kpts=(12,12,12)
code='Qunatum-Espresso'

metal =  'La'
metal2 =  'Bi'
a=5.039406441
c=5.039406441
crystal = 'fcc'
name=metal+'2'+metal2+'2'
atoms=Atoms(name,scaled_positions=[(0,0,0),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5)],cell=[a,a,c],pbc=True)
atoms.set_pbc((1,1,1)) 

calc = espresso(pw=pw,
                dw=dw,   
                xc=xc,   
                kpts=kpts, 
                nbands=-20, 
                sigma=0.1,
                calcstress=True,
                spinpol=False,
                convergence= {'energy':1e-5,    #convergence parameters
                              'mixing':0.1,
                              'nmix':10,
                              'mix':4,
                              'maxsteps':500,
                              'diag':'david'
                              }, 
                psppath='/home/mamunm/src/pseudo/gbrv1.5pbe',
                outdir='cell_relax',
                mode='vc-relax',cell_factor=2,
                cell_dynamics='bfgs',
                opt_algorithm='bfgs',
                output = {'avoidio':True,'removewf':True,'wf_collect':False})

atoms.set_calculator(calc) 

print 'Potential_Energy:', atoms.get_potential_energy(), 'eV'
print 'Kinetic_Energy:', atoms.get_kinetic_energy(), 'eV'
print 'Total_Energy:', atoms.get_total_energy(), 'eV'

