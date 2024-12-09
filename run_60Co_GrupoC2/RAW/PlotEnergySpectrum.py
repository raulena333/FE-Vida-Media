import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os

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

# Names of nucleus isotopes
channels = ["0", "1"]

# Output directory
output_dir = './run_60Co_GrupoC2/Results'
os.makedirs(output_dir, exist_ok=True)

# Function to plot channel spectrum
def plot_spectrum(name, channel_number, net_counts):
    plt.figure(figsize=(10, 6))
    plt.plot(channel_number, net_counts, label=name, color="black")
    plt.xlabel("Energia (keV)")
    plt.xlim(0, 2000)
    plt.ylabel("Número de cuentas")
    plt.legend()

    if use_log_scale:
        plt.semilogy()
        suffix = '_CoEnergySpectreLog.pdf'
    else:
        suffix = '_CoEnergySpectre.pdf'
    plt.savefig(os.path.join(output_dir, name + suffix))
    plt.show()

# Process each nucleus
for ch in channels:
    file_path = f'./run_60Co_GrupoC2/RAW/CH{ch}@DT5751_11655_EspectrumRErrorsEnergies_run_60CoGrupoC2_20241114_134013.txt'
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping channel {ch}.")
        continue

    # Load data for the nucleus
    try:
        data_nucleus = np.loadtxt(file_path, skiprows = 1)
        counts = data_nucleus[:,0]
        energies = data_nucleus[:,2]

        # Plot spectrum
        plot_spectrum(f"Detector {ch}", energies, counts)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")