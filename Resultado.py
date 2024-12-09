import numpy as np

# Given values for the slope and its uncertainty
slope = 0.116569  # Slope value from the exponential fit
slope_error = 0.0044064  # Uncertainty in the slope

# Calculate the half-life (T_half) using the formula T_half = ln(2) / slope
half_life = np.log(2) / slope
real_value = 6.283

# Calculate the uncertainty in the half-life using error propagation
# Formula: ΔT_half = (ln(2) / slope^2) * Δslope
half_life_error = (np.log(2) / slope**2) * slope_error

# Calculate the relative error
relative_error = abs(real_value - half_life) / real_value * 100

# Print the results
print(f"Calculated half-life: {half_life:.6f} +- {half_life_error:.6f} ns")
print(f"Relative error is: {relative_error}")
