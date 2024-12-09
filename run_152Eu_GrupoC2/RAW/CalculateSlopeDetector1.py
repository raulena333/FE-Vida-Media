import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os
from scipy.optimize import curve_fit

# Configure parameters for plot appearance
params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params)

# Quadratic function definition
def quadratic_func(x, a, b, c):
    return a * x**2 + b * x + c

# Output file paths
output_plot = './run_152Eu_GrupoC2/Results/EnergyDetector1_calibration.pdf'
param_file = './run_152Eu_GrupoC2/Results/Quadratic_fit_parametersDetector1.txt'

# Function to read the xc, its error, and energy from the file
def read_parameters(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    xc = None
    xc_err = None
    energy = None

    # Parse lines to extract values
    for line in lines:
        if "xc (peak center)" in line:
            xc = float(line.split(':')[1].split('+-')[0].strip())
            xc_err = float(line.split('+-')[1].split()[0].strip())
        if "Gaussian peak energy" in line:
            energy = float(line.split(':')[1].split()[0])
    
    # Check for missing values
    if xc is None or xc_err is None or energy is None:
        raise ValueError("Failed to extract xc, xc_err, or energy from the file.")
    
    return xc, xc_err, energy

# Process the files and perform calibration
files = [
    "./run_152Eu_GrupoC2/Results/Ch1energy1_fitted_parameters.txt",
    "./run_152Eu_GrupoC2/Results/Ch1energy2_fitted_parameters.txt",
    "./run_152Eu_GrupoC2/Results/Ch1energy3_fitted_parameters.txt",
    "./run_152Eu_GrupoC2/Results/Ch1energy4_fitted_parameters.txt",
    "./run_152Eu_GrupoC2/Results/Ch1energy5_fitted_parameters.txt",
    "./run_152Eu_GrupoC2/Results/Ch1energy6_fitted_parameters.txt",
    "./run_152Eu_GrupoC2/Results/Ch1energy7_fitted_parameters.txt",
]

# Arrays to hold extracted values
xcs = []
xc_errors = []
energies = []

for file_name in files:
    if not os.path.exists(file_name):
        print(f"File {file_name} does not exist. Skipping.")
        continue

    try:
        # Read parameters from the file
        xc, xc_err, energy = read_parameters(file_name)
        xcs.append(xc)
        xc_errors.append(xc_err)
        energies.append(energy)
    except ValueError as e:
        print(f"Error while processing {file_name}: {e}")
        continue

# Convert to NumPy arrays for processing
xcs = np.array(xcs)
xc_errors = np.array(xc_errors)
energies = np.array(energies)

# Perform quadratic fit
try:
    popt, pcov = curve_fit(quadratic_func, xcs, energies, sigma=xc_errors, absolute_sigma=True)
    a, b, c = popt
    errors = np.sqrt(np.diag(pcov))
    a_err, b_err, c_err = errors

    # Generate fitted curve for plotting
    channel_range = np.linspace(0, max(xcs) * 1.2, 500)  # Extend a bit beyond the max channel
    fitted_energies = quadratic_func(channel_range, a, b, c)

    # Plot the calibration
    plt.figure(figsize=(10, 6))
    plt.errorbar(xcs, energies, yerr=xc_errors, fmt='.', markersize=6, color="#074936", 
                 elinewidth=1.5, ecolor="#000000", label="Data", capsize=3)
    plt.plot(channel_range, fitted_energies, color="#AD3628", linewidth=2, linestyle="solid", label="Fit Cuadratico")

    # Labels and legend
    plt.xlabel("Canal")
    plt.ylabel("Energia (keV)")
    plt.legend()

    # Add the quadratic formula as text annotation on the plot
    formula_text = f"$y = ({a:.4e}) x^2 + ({b:.4e}) x + ({c:.4e})$"
    plt.text(0.05, 0.95, formula_text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')

    # Save the plot
    os.makedirs(os.path.dirname(output_plot), exist_ok=True)
    plt.savefig(output_plot)
    plt.close()
    print(f"Energy calibration plot saved as {output_plot}")

    # Save the fitted parameters to a text file
    with open(param_file, 'w') as f:
        f.write(f"Fitted parameters for quadratic energy calibration:\n")
        f.write("------------------------------------------------\n")
        f.write(f"a (quadratic term): {a:.6f} +- {a_err:.6f}\n")
        f.write(f"b (linear term): {b:.6f} +- {b_err:.6f}\n")
        f.write(f"c (constant term): {c:.6f} +- {c_err:.6f}\n")
        f.write("------------------------------------------------\n")
    print(f"Fitted quadratic parameters saved to {param_file}")

except RuntimeError as e:
    print(f"Curve fitting failed: {e}")

