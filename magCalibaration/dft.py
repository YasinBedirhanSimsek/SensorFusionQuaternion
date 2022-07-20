from cmath import cos, pi
from math import sin
import numpy as np
import matplotlib.pyplot as plot
import scipy as sp
import scipy.fft as spftt


f1 = 0.25
f2 = 3.0/8.0

n = np.linspace(1, 8, 8)

x = 0.5 * np.cos(2*pi*f1*n) + np.sin(2*pi*f2*n)

print(x)

fft_x = spftt.fft(x)
shifted_fft_x = spftt.fftshift(fft_x)

#plot.stem(n, np.abs(fft_x))
plot.stem(n, np.abs(shifted_fft_x))
plot.show()

