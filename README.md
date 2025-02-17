# RASPA2 tutorial: how to run RASPA from python
work in progress..

## 2. run auto
check the hard coded x,y,z coordinates of the molecule in run_auto.

just run
'''
bash run_auto
'''

## 3. same result (just numerical values)

just run
'''
bash run_from_python.sh 5.0 0 0 
'''

or run the **calc_ext_pot_with_raspa_3D_cif_grid.py** script to calculate a whole cif file on a cDFT grid (with density of 2 gridpoints per Å). make sure you replicate the unitcell often enough in simulation.input. 
