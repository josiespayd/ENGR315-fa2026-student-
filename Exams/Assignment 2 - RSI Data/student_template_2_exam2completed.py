"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import ttest_1samp
from scipy.stats import norm
from scipy.stats import chisquare
from scipy.stats import t
from scipy.stats import sem


# Find the folder where this Python file is saved & create path to the data file
folder = os.path.dirname(__file__)
path_to_file = os.path.join(folder, '../../data/drop-jump/all_participant_data_rsi.csv')

# Load the RSI data & Print the data

df = pd.read_csv(path_to_file)
print(df)

# Task 1: T-test
print("\nTask 1: T-test")
force_plate_rsi = df['force_plate_rsi'].to_numpy()
accelerometer_rsi = df['accelerometer_rsi'].to_numpy()
difference = force_plate_rsi - accelerometer_rsi
alpha = 0.05
(stat, p_value) = ttest_1samp(difference, popmean=0, alternative='two-sided')
print('H0: mean paired difference=0')
print('H1: mean paired difference is not equal to 0')
print('t-value:', stat)
print('p-value:', p_value)
if p_value < alpha:
    print('Reject H0: The methods have a significantly different mean RSI')
else:
    print('Fail to reject H0: The methods do not have a significantly different mean RSI')

# Task 2: Normal distribution fit test
print("\nTask 2: Normal distribution fit test")
(fitted_mean, fitted_std) = norm.fit(accelerometer_rsi)
print('Fitted mean:', fitted_mean)
print('Fitted standard deviation:', fitted_std)

# Bins
bin_edges = np.linspace(fitted_mean - fitted_std, fitted_mean + fitted_std, 5)
bins = np.r_[-np.inf,bin_edges,np.inf]
observed_counts, observed_edges = np.histogram(accelerometer_rsi, bins=bins, density=False)
expected_counts = np.diff(norm.cdf(bins, loc=fitted_mean, scale=fitted_std))
expected_counts = expected_counts * len(accelerometer_rsi)
(chi_stat, chi_p_value) = chisquare(f_obs=observed_counts,f_exp=expected_counts,ddof=2)
print('Observed counts:', observed_counts)
print('Expected counts:', expected_counts)
print('Chi-square statistic:', chi_stat)
print('Chi-square p-value:', chi_p_value)
if min(expected_counts) < 5:
    print('Warning: at least one expected count is below 5, may affect the validity of the test')
if chi_p_value < alpha:
    print('Reject H0: The normal distribution is not a good fit')
else:
    print('Fail to reject H0: No evidence of a poor normal fit')

plt.hist(accelerometer_rsi, bins=10, density=True, label='Accelerometer RSI', edgecolor='black')
x = np.linspace(min(accelerometer_rsi), max(accelerometer_rsi), 1000)
y = norm.pdf(x, loc=fitted_mean, scale=fitted_std)
plt.plot(x,y,label='Fitted Normal Distribution')
plt.xlabel('Accelerometer RSI')
plt.ylabel('Probability Density')
plt.title('Accelerometer RSI and Fitted Normal Distribution')
plt.legend()
plt.show()

# Task 3: F trials and 95% confidence interval
print("\nTask 3: F trials and 95% confidence interval")
participant_f = df[df['trial'].str.startswith('F_')]
print(participant_f)

f_force = participant_f['force_plate_rsi']
f_accelerometer = participant_f['accelerometer_rsi']

force_mean = f_force.mean()
accelerometer_mean = f_accelerometer.mean()
(force_lower, force_upper) = t.interval(confidence=0.95, df=len(f_force)-1,loc=force_mean, scale=sem(f_force))
(accel_lower, accel_upper) = t.interval(confidence=0.95, df=len(f_accelerometer)-1,loc=accelerometer_mean, scale=sem(f_accelerometer))
print('Forceplate mean:',force_mean)
print('Force plate 95% CI:', force_lower, 'to', force_upper)
print('Accelerometer mean:',accelerometer_mean)
print('Accelerometer 95% CI:', accel_lower, 'to', accel_upper)

