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

use_log_scale = True  # True for log scale, False for linear scale

# Names of nucleus isotopes and their excitation energies
energy_europio = {
    'Ch1energy1': {'Energy': 1173.228, 'min': 1076, 'max': 1151},
    'Ch1energy2': {'Energy': 1332.492, 'min': 1151, 'max': 1228},
}

# Define specific initial guesses for each energy
initial_guesses = {
    'Ch1energy1': [-1., -3., 3.6e3, 1107, 3],
    'Ch1energy2': [-1., -3., 3e3, 1190, 3],
}

# Load data for the nucleus
file_path = './run_60Co_GrupoC2/RAW/CH1@DT5751_11655_EspectrumRErrors_run_60CoGrupoC2_20241114_134013.txt'
if not os.path.exists(file_path):
    print(f"File {file_path} does not exist.")
    exit()

# Load data for the nucleus
try:
    data_nucleus = np.loadtxt(file_path, skiprows=1)
    counts = data_nucleus[:, 0]
    error = data_nucleus[:, 1]
    channel = np.arange(0, len(data_nucleus))
except Exception as e:
    print(f"Error processing file {file_path}: {e}")
    exit()

# Output directory for results and plots
output_dir = './run_60Co_GrupoC2/Results'
os.makedirs(output_dir, exist_ok=True)

# Define a Gaussian with background linear term for fitting
def gaussian(x, a, b, c, xc, s): 
    return a + b * x + c * np.exp(-(x - xc)**2 / (2 * s**2))

plt.figure(figsize=(10, 6))
plt.plot(channel, counts, label="Espectro detector 1", color="black", linewidth=1)
    
# Process each energy
for name, props in energy_europio.items():
    min_channel = props['min']
    max_channel = props['max']

    # Select data within the region of interest (from min to max)
    region = (channel >= min_channel) & (channel <= max_channel)
    channels_in_region = channel[region]
    counts_in_region = counts[region]
    error_in_region = error[region]

    # Retrieve the initial guess for this energy
    initial_guess = initial_guesses[name]

    # Fit the model (Gaussian + Linear background) to the data
    try:
        popt, pcov = curve_fit(
            gaussian,
            channels_in_region,
            counts_in_region,
            p0=initial_guess,
            sigma=error_in_region
        )
        # Calculate parameter errors as the square root of the diagonal of the covariance matrix
        perr = np.sqrt(np.diag(pcov))
    except RuntimeError as e:
        print(f"Curve fitting failed for {name}: {e}. Skipping this energy.")
        continue

    # Extract fitted parameters and their errors
    a, b, c, xc, s = popt
    a_err, b_err, c_err, xc_err, s_err = perr

    # Generate the fitted curve
    fitted_curve = gaussian(channels_in_region, *popt)

    # Save the fitted parameters and errors to a text file
    param_file = os.path.join(output_dir, f'{name}_fitted_parameters.txt')
    with open(param_file, 'w') as f:
        f.write(f"Fitted parameters for {name}:\n")
        f.write("------------------------------------------------\n")
        f.write(f"a (offset): {a:.4f} +- {a_err:.4f}\n")
        f.write(f"b (background slope): {b:.4f} +- {b_err:.4f}\n")
        f.write(f"c (peak height): {c:.4f} +- {c_err:.4f}\n")
        f.write(f"xc (peak center): {xc:.4f} +- {xc_err:.4f} channel\n")
        f.write(f"s (peak width): {s:.4f} +- {s_err:.4f} channel\n")
        f.write("------------------------------------------------\n")
        f.write(f"Gaussian peak energy: {props['Energy']} keV\n")
    print(f"Fitted parameters and errors for {name} saved to {param_file}")

    # Plot the spectrum with the fitted Gaussian and background
    plt.plot(channels_in_region, fitted_curve, color="red", linestyle='--', linewidth=2, #label=f"{name} Fit"
             )
    
# Finalize the combined plot    
plt.xlabel("Canal")
plt.xlim(0, 2000)
plt.ylabel("Número de cuentas")
plt.legend()

# Apply log scale if specified
if use_log_scale:
    plt.semilogy()
    suffix = '_FitLog.pdf'
else:
    suffix = '_Fit.pdf'

# Save the plot to the specified directory
plot_file_path = os.path.join(output_dir, name + suffix)
plt.savefig(plot_file_path)
plt.close()
print(f"Plot saved for {name} as {plot_file_path}")
