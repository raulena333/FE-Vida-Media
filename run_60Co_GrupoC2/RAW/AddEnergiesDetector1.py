import numpy as np
import os

# Path to the quadratic fit parameters file
quadratic_fit_file = './run_60Co_GrupoC2/Results/Quadratic_fit_parametersDetector1.txt'

def read_quadratic_params(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize variables for parameters and errors
    a = b = c = None
    a_err = b_err = c_err = None
    
    # Parse lines to extract values for a, b, c and their errors
    for line in lines:
        if "a (quadratic term):" in line:
            a = float(line.split(':')[1].split('+-')[0].strip())
            a_err = float(line.split('+-')[1].split()[0].strip())  # Extract the error for 'a'
        if "b (linear term):" in line:
            b = float(line.split(':')[1].split('+-')[0].strip())
            b_err = float(line.split('+-')[1].split()[0].strip())  # Extract the error for 'b'
        if "c (constant term):" in line:
            c = float(line.split(':')[1].split('+-')[0].strip())
            c_err = float(line.split('+-')[1].split()[0].strip())  # Extract the error for 'c'
    
    # Check if all parameters and their errors were found
    if a is None or b is None or c is None or a_err is None or b_err is None or c_err is None:
        raise ValueError("Failed to extract quadratic parameters (a, b, c) and their errors from the file.")
    
    return a, a_err, b, b_err, c, c_err

# Example usage
quadratic_fit_file = './run_60Co_GrupoC2/Results/Quadratic_fit_parametersDetector1.txt'

try:
    a, a_err, b, b_err, c, c_err = read_quadratic_params(quadratic_fit_file)
    print(f"Quadratic parameters and errors read from file:\n a = {a:.6f} ± {a_err:.6f}\n b = {b:.6f} ± {b_err:.6f}\n c = {c:.6f} ± {c_err:.6f}")
except ValueError as e:
    print(f"Error reading quadratic parameters: {e}")
    exit()
    
    
# Process each detector
file_path = f'./run_60Co_GrupoC2/RAW/CH1@DT5751_11655_EspectrumRErrors_run_60CoGrupoC2_20241114_134013.txt'
output_file = f'./run_60Co_GrupoC2/RAW/CH1@DT5751_11655_EspectrumRErrorsEnergies_run_60CoGrupoC2_20241114_134013.txt'
    
# Load data for the nucleus
data_nucleus = np.loadtxt(file_path, skiprows=1)
nucleus_counts = data_nucleus[:, 0]
error = data_nucleus[:, 1]
channel = np.arange(0, len(data_nucleus))

# Transform channels to energy using the quadratic formula
energy = a * channel**2 + b * channel + c
error_energy = np.sqrt((2 * a *channel * a_err)**2 + (b * b_err)**2)

# Combine original data with the energy column
data_with_energy = np.column_stack((data_nucleus, energy, error_energy))

# Save the new data to a file
header = "Counts\tError\tEnergy (keV)\t ErrorEnergy"
np.savetxt(output_file, data_with_energy, header=header, fmt=['%.0f', '%.4f', '%.3f', '%.15f'], delimiter='\t')
print(f"File with energy column saved: {output_file}")


