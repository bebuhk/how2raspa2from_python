"""
Author: Benedikt Buhk 
Date: 2025-02-07
Description: calculate the external potential for a grid inside a unitcell with RASPA2 (through the bash script run_from_python.sh)
"""

import numpy as np
import pandas as pd
import subprocess
import time
from pymatgen.io.cif import CifParser

t0 = time.time()


#cif_path = 'RSM0107_modified.cif'
#cif_path = 'test.cif'
#cif_path = 'RSM0177.cif'
cif_path = 'RSM0290.cif'

res_path = 'zz_results/RSM0290_20_3_3_3.csv'

assert cif_path.split(".")[0] in res_path, f"Error: The cif file {cif_path} is not the same as the one in the result path {res_path}"

# check if the line in simulation.input containing FrameworkName also contains cif_path
with open('simulation.input') as f:
    lines = f.readlines()
    for line in lines:
        if 'FrameworkName' in line:
            print(line)
            if cif_path.split(".")[0] not in line:
                print(f"Error: The cif file {cif_path} is not the same as the one in simulation.input")
                exit()
            else:
                # leave for looop
                break


cif_parser = CifParser(cif_path, occupancy_tolerance=100)
structure_adsorbent = cif_parser.parse_structures(primitive=False)[0]
a = structure_adsorbent.lattice.a
b = structure_adsorbent.lattice.b
c = structure_adsorbent.lattice.c
alpha_rad = structure_adsorbent.lattice.angles[0] * 2 * np.pi / 360
beta_rad = structure_adsorbent.lattice.angles[1] * 2 * np.pi / 360
gamma_rad = structure_adsorbent.lattice.angles[2] * 2 * np.pi / 360
alpha_deg = structure_adsorbent.lattice.angles[0]
beta_deg = structure_adsorbent.lattice.angles[1]
gamma_deg = structure_adsorbent.lattice.angles[2]
# from get_lattice_RASPA
xi = (
    np.cos(alpha_rad) - np.cos(gamma_rad) * np.cos(beta_rad)
) / np.sin(gamma_rad)
lat_test = np.array(
    [
        [
            a,
            b * np.cos(gamma_rad),
            c * np.cos(beta_rad),
        ],
        [0, b * np.sin(gamma_rad), c * xi],
        [0, 0, c * np.sqrt(1 - np.cos(beta_rad) ** 2 - xi**2)],
    ]
)
lattice = lat_test.T
lattice
a1 = lattice[0,:]
a2 = lattice[1,:]
a3 = lattice[2,:]


print(f"a1={a1}, a2={a2}, a3={a3}")
# end script
#exit()

# a1 = np.array([10,0,0])
# a2 = np.array([5,10,0])
# a3 = np.array([0,0,10])

resolution = 20
R1,R2,R3 = np.meshgrid(np.linspace(0,1,resolution),np.linspace(0,1,resolution),np.linspace(0,1,resolution))
X = a1[0]*R1+a2[0]*R2+a3[0]*R3
Y = a1[1]*R1+a2[1]*R2+a3[1]*R3
Z = a1[2]*R1+a2[2]*R2+a3[2]*R3

energy = np.zeros((resolution,resolution,resolution))
LJ = np.zeros((resolution,resolution,resolution))
Coulomb_ewald = np.zeros((resolution,resolution,resolution))
Coulomb_real = np.zeros((resolution,resolution,resolution))
Coulomb_fourier = np.zeros((resolution,resolution,resolution))
alpha = np.zeros((resolution,resolution,resolution))

for i in range(resolution):
    for j in range(resolution):  
        for k in range(resolution):
            # Run the Bash script with the numbers as arguments
            print(f"x={X[i,j,k]};  \ty={Y[i,j,k]};  \tz={Z[i,j,k]}")
            #print(f"str(X[i,j])={str(X[i,j])}, str(Y[i,j])={str(Y[i,j])}")
            try:
                result = subprocess.run(
                    ["./run_from_python.sh", '--', str(X[i,j,k]), str(Y[i,j,k]), str(Z[i,j,k])], #, "0", "0", "10"], #
                    #["./run_from_python.sh", '--', str(-0.49384578947368496), str(0.0), str(0.0)], #, "0", "0", "10"], #
                    
                    check=True,  # Raise an exception if the script fails
                    text=True,   # Decode stdout/stderr as text
                    capture_output=True  # Capture stdout and stderr
                )
                script_output = result.stdout.split()
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                # Handle errors if the script fails
                print(f"Error running the Bash script: {e}")
                print(f"Script stderr: {e.stderr}")    
        #script_output = !bash run_from_python.sh {X[i,j]} {Y[i,j]} 0 ## only works from ipynb
            #print(f"x={X[i,j,k]};  \ty={Y[i,j,k]};  \tz={Z[i,j,k]}")
            #script_output = !bash run_from_python.sh {X[i,j,k]} {Y[i,j,k]} {Z[i,j,k]}
            energy[i,j,k] = float(script_output[0])
            LJ[i,j,k] = float(script_output[1])
            Coulomb_ewald[i,j,k] = float(script_output[2])
            Coulomb_real[i,j,k] = float(script_output[3])
            Coulomb_fourier[i,j,k] = float(script_output[4])
            alpha[i,j,k] = float(script_output[5])

df = pd.DataFrame(data = {'X':X.flatten(),'Y':Y.flatten(), 'Z':Z.flatten(),'energy':energy.flatten(),'LJ':LJ.flatten(),\
        'Coulomb_ewald':Coulomb_ewald.flatten(),'Coulomb_real':Coulomb_real.flatten(), \
            'Coulomb_fourier':Coulomb_fourier.flatten(), 'alpha':alpha.flatten()})
#df.to_csv('zz_results/RSM0177_1_1_1_reproduced.csv',index=False)
df.to_csv(res_path,index=False)

t1 = time.time()
print(f"Time elapsed: {t1-t0} s")