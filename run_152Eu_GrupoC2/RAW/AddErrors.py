import numpy as np
import os

use_log_scale = True  # True for log scale, False for linear scale

# Names of nucleus isotopes
channels = ["0", "1"]

# Output directory
output_dir = './run_152Eu_GrupoC2/Raw'

# Process each nucleus
for ch in channels:
    file_path = f'./run_152Eu_GrupoC2/RAW/CH{ch}@DT5751_11655_EspectrumR_run_152Eu_GrupoC2_20241114_131404.txt'
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping channel {ch}.")
        continue

    # Load data for the nucleus
    try:
        data_nucleus = np.loadtxt(file_path)
        error_counts = np.sqrt(data_nucleus)
        
        data_error = np.column_stack((data_nucleus, error_counts))
        output_file = f'./run_152Eu_GrupoC2/RAW/CH{ch}@DT5751_11655_EspectrumRErrors_run_152Eu_GrupoC2_20241114_131404.txt'
        np.savetxt(output_file, data_error, header="Net Counts\tError", fmt=['%.0f', '%.4f'], delimiter='\t')

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
