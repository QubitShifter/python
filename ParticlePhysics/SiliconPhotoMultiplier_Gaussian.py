import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from scipy.optimize import curve_fit

#%matplotlib ipympl

def gauss(x, amp, cen, sig):
    return amp * np.exp(-(x - cen)**2 / (2 * sig**2))

def multi_gauss(x, *args):
    return sum(gauss(x, *args[i:i+3]) for i in range(0, len(args), 3))

filename = '_70.10.xlsx'


df = pd.read_excel(filename)
x_values = df.iloc[:, 0]
y_values = df.iloc[:, 1]

plt.style.use('seaborn')
plt.figure(figsize = (10, 6))

plt.scatter(x_values, y_values, marker = '.')

plt.title('SiPM спектър')
plt.xlabel('Канал')
plt.ylabel('Брой събития')
plt.grid(True)
plt.show()

lower_fit_bound = -40
upper_fit_bound = 60
peak_distance = 180
n_peaks = 10

lower_range = [lower_fit_bound + i*peak_distance for i in range(0, n_peaks)]
upper_range = [upper_fit_bound + i*peak_distance for i in range(0, n_peaks)]

initial_guess = []
for i in range(0, len(lower_range)):
    x_filtered = x_values[(x_values >= lower_range[i]) & (x_values <= upper_range[i])]
    y_filtered = y_values[(x_values >= lower_range[i]) & (x_values <= upper_range[i])]

    mean_x = np.mean(x_filtered)
    std_dev_x = np.std(x_filtered)

initial_guess.extend([np.max(y_filtered), mean_x, std_dev_x])
popt, pcov = curve_fit(multi_gauss, x_values, y_values, p0=initial_guess)
gauss_components = [multi_gauss(x_values, *popt[i:i+3]) for i in range(0, len(popt), 3)]

plt.style.use('seaborn')
plt.figure(figsize=(10, 6))

plt.scatter(x_values, y_values, marker='.', label='Original data')
plt.plot(x_values, sum(gauss_components), 'r-', linewidth=3, label='Fitted MultiGauss')
plt.legend()

plt.title('SiPM Spectrum')
plt.xlabel('Channel Number')
plt.ylabel('Event Counts')

plt.grid(True)
plt.show()

gauss_components = []
for i in range(0, len(popt), 3):
    gaussian_parameters.append((popt[i], popt[i+1], popt[i+2]))

for i, (num, cen, sig) in enumerate(gaussian_parameters, start = 1):
    print(f"Gaussins {I}:\nMean = {cen}\nSigma = {sig}\n")