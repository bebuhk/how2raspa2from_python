#!/Users/bene/miniconda3/envs/ase/bin/python
"""
Author: Benedikt Buhk 
Date: 2025-02-07
Description: calculate the external potential for a grid inside a unitcell with RASPA2 (through the bash script run_from_python.sh)
"""

import numpy as np
import pandas as pd

import subprocess

try:
    result = subprocess.run(
        ["./run_from_python.sh", "0"],
        check=True,  # Raise an exception if the script fails
        text=True,   # Decode stdout/stderr as text
        capture_output=True  # Capture stdout and stderr
    )
    script_output = result.stdout.split()
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Script failed with exit code {e.returncode}")
    print(f"Script stderr: {e.stderr}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
