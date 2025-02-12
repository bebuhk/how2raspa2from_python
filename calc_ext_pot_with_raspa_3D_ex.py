"""
Author: Benedikt Buhk 
Date: 2025-02-07
Description: calculate the external potential for a grid inside a unitcell with RASPA2 (through the bash script run_from_python.sh)
"""

import numpy as np
import pandas as pd
import subprocess
import time

t0 = time.time()

a1 = np.array([10,0,0])
a2 = np.array([5,10,0])
a3 = np.array([0,0,10])

print(f"a1={a1}, a2={a2}, a3={a3}")
# end script
#exit()

resolution = 3
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
                    ["./run_from_python.sh", str(X[i,j,k]), str(Y[i,j,k]), str(Z[i,j,k])], #, "0", "0", "10"], #
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
df.to_csv('zz_results/test_cif_3_mesh.csv',index=False)

t1 = time.time()
print(f"Time elapsed: {t1-t0} s")