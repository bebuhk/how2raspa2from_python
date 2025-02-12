#!/Users/bene/miniconda3/envs/ase/bin/python
"""
Author: Benedikt Buhk 
Date: 2025-02-07
Description: calculate the external potential for a grid inside a unitcell with RASPA2 (through the bash script run_from_python.sh)
"""

import numpy as np
import pandas as pd
import subprocess



#script_output = !bash run_from_python.sh {X[0,0]} {Y[0,0]} 0 # this works only from jupyter notebook

# Three numbers to pass as arguments
number1 = "0"
number2 = "0"
number3 = "0"

# Run the Bash script with the numbers as arguments
try:
    result = subprocess.run(
        ["./run_from_python_test.sh", number1, number2, number3],
        check=True,  # Raise an exception if the script fails
        text=True,   # Decode stdout/stderr as text
        capture_output=True  # Capture stdout and stderr
    )
    # Print the output of the Bash script
    print("Bash script output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    # Handle errors if the script fails
    print(f"Error running the Bash script: {e}")
    print(f"Script stderr: {e.stderr}")

print("hi")
#print(result.stdout)
print("bye")

