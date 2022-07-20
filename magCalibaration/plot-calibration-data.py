"""

PLOT UNCALIBRTED AND CALIBRATED MAGNETOMETER MEASUREMENTS

Read data file with raw measurements and compare calibrated vs. uncalibrated
measurements.

Code By: Michael Wrona
Created: 14 Jan 2021

The calibration equation is:
    h_calib = A * (h_meas - b)

h_calib: Calibrated measurements (3x1)
A: Soft iron, scale factor, and misalignment correction matrix (3x3, symmetric)
h_meas: Raw measurements (3x1)
b: Hard-iron offset correction vector (3x1)

Calibration parametrers were determined by the Magneto calibration software (see below).

Resources
---------

Magnetometer/IMU I used:
    https://www.adafruit.com/product/3463

Magneto magnetometer calibration software download:
    https://sites.google.com/site/sailboatinstruments1/home

"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

from RCFilter import RCFilter

A = np.array(   [[  0.579694,  0.027833,  0.059762],
                [   0.027833,  0.550316,  0.111774],
                [   0.059762,  0.111774,  0.613258]])

b = np.array(     [0.249145, 0.343886, 0.420939])

A = np.array(   [[  2.122474,  -0.034716,  0.111930],
                [  -0.034716,   1.920829, -0.094700],
                [   0.111930,  -0.094700,  2.421364]])

b = np.array(     [-0.137891, -0.065138, 0.032906])

A = np.array(   [[  2.078310,   0.045795,  0.014359],
                [   0.045795,   2.014685,  0.004263],
                [   0.014359,   0.004263,  2.200746]])

b = np.array(     [-0.091492, -0.021514, 0.053752])

rcf_0:RCFilter = RCFilter(5, 0.01)
rcf_1:RCFilter = RCFilter(5, 0.01)

# Read raw data and apply calibration
rawData = np.genfromtxt('.\examples\\1_acc_mpu6050.txt', delimiter='\t')  # Read raw measurements

filtered_uncalibrated = np.zeros(rawData.shape)
filtered_calibrated = np.zeros(rawData.shape)

N = len(rawData)
calibData = np.zeros((N, 3), dtype='float')
for i in range(N):
    currMeas = np.array([rawData[i, 0], rawData[i, 1], rawData[i, 2]])
    calibData[i, :] = A @ (currMeas - b)

    filtered_uncalibrated[i] = rcf_0.RCFilter_Update(currMeas)
    filtered_calibrated[i]   = rcf_1.RCFilter_Update(calibData[i, :])

np.savetxt("input.csv", rawData, delimiter=",")
np.savetxt("input_filtered.csv", filtered_uncalibrated[50:,], delimiter=",")
np.savetxt("output.csv", calibData, delimiter=",")
np.savetxt("output_filtered.csv", filtered_calibrated[50:,], delimiter=",")

# Plot XY data
plt.figure()
plt.plot(rawData[:, 0], rawData[:, 1], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 0], calibData[:, 1], 'r*', label='Calibrated Meas.')
##plt.plot(filtered_uncalibrated[50:, 0], filtered_uncalibrated[50:, 1], 'y*', label='Filtered Unalibrated Meas.')
##plt.plot(filtered_calibrated[50:, 0],   filtered_calibrated[50:, 1],   'g*', label='Filtered Calibrated Meas.')
plt.title('XY Magnetometer Data')
plt.xlabel('X [uT]')
plt.ylabel('Y [uT]')
plt.legend()
plt.grid()
plt.axis('equal')

# Plot YZ data
plt.figure()
plt.plot(rawData[:, 1], rawData[:, 2], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 1], calibData[:, 2], 'r*', label='Calibrated Meas.')
#plt.plot(filtered_uncalibrated[50:, 1], filtered_uncalibrated[50:, 2], 'y*', label='Filtered Unalibrated Meas.')
#plt.plot(filtered_calibrated[50:, 1],   filtered_calibrated[50:, 2],   'g*', label='Filtered Calibrated Meas.')
plt.title('YZ Magnetometer Data')
plt.xlabel('Y [uT]')
plt.ylabel('Z [uT]')
plt.legend()
plt.grid()
plt.axis('equal')

# Plot XZ data
plt.figure()
plt.plot(rawData[:, 0], rawData[:, 2], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 0], calibData[:, 2], 'r*', label='Calibrated Meas.')
#plt.plot(filtered_uncalibrated[50:, 0], filtered_uncalibrated[50:, 2], 'y*', label='Filtered Unalibrated Meas.')
#plt.plot(filtered_calibrated[50:, 0],   filtered_calibrated[50:, 2],   'g*', label='Filtered Calibrated Meas.')
plt.title('XZ Magnetometer Data')
plt.xlabel('X [uT]')
plt.ylabel('Z [uT]')
plt.legend()
plt.grid()
plt.axis('equal')

calibGraphData = go.Scatter3d(
    x=calibData[:,0], 
    y=calibData[:,1], 
    z=calibData[:,2], 
    marker=go.scatter3d.Marker(size=3), 
    opacity=0.8, 
    mode='lines'
)

uncalibGraphData = go.Scatter3d(
    x=rawData[:,0], 
    y=rawData[:,1], 
    z=rawData[:,2], 
    marker=go.scatter3d.Marker(size=4), 
    opacity=0.8, 
    mode='lines',
) 

uncalibGraphData_filtered = go.Scatter3d(
    x=rawData[:,0], 
    y=rawData[:,1], 
    z=rawData[:,2], 
    marker=go.scatter3d.Marker(size=4), 
    opacity=0.8, 
    mode='lines'
) 

calibGraphData_filtered = go.Scatter3d(
    x=filtered_calibrated[:,0], 
    y=filtered_calibrated[:,1], 
    z=filtered_calibrated[:,2], 
    marker=go.scatter3d.Marker(size=4), 
    opacity=0.8, 
    mode='lines',
) 

fig=go.Figure(data=(calibGraphData,uncalibGraphData, calibGraphData_filtered))
fig.show()

fig.show()

plt.show()
