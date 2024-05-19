"""
Dans_Diffraction Tests
Compare alternate methods of creating gaussian meshes
"""

import os, time
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

import Dans_Diffraction as dif

xtl = dif.structure_list.Ca2RuO4()
#xtl = xtl.generate_superstructure([[7,0,0],[0,7,0],[0,0,1]])

t00 = time.time()
Qx, Qy, HKL = xtl.Cell.reciprocal_space_plane()#[1,0,0], [0,1,0], [0,0,0], 4, 0.1)
t01 = time.time()
I = xtl.Scatter.intensity(HKL)
t02 = time.time()
print('Reciprocal space plane took: %s s' % (t01-t00))
print('intensity took: %s s' % (t02-t01))
print('Number of reflections: %d' % len(HKL))

q_max = 4.0
pixels = 201  # reduce this to make convolution faster
pixel_size = (2.0 * q_max) / pixels
mesh_all = np.zeros([pixels, pixels])
mesh = np.zeros([pixels, pixels])
mesh_x = np.linspace(-q_max, q_max, pixels)
X, Y = np.meshgrid(mesh_x, mesh_x)

# add reflections to background
pixel_i = ((Qx / (2 * q_max) + 0.5) * pixels).astype(int)
pixel_j = ((Qy / (2 * q_max) + 0.5) * pixels).astype(int)
#pixel_i = np.round((Qx / (2 * q_max) + 0.5) * pixels).astype(int)
#pixel_j = np.round((Qy / (2 * q_max) + 0.5) * pixels).astype(int)

mesh_all[pixel_j, pixel_i] = np.ones(len(I))
mesh[pixel_j, pixel_i] = I

peak_width = pixel_size/2

# Convolve2d
t1 = time.time()
mesh_convolve = np.zeros([pixels, pixels])
mesh_convolve[pixel_j, pixel_i] = I
peak_width_pixels = peak_width / pixel_size
gauss_x = np.arange(-3 * peak_width_pixels, 3 * peak_width_pixels + 1)
G = dif.fg.gauss(gauss_x, gauss_x, height=1, centre=0, fwhm=peak_width_pixels, bkg=0)
mesh_convolve = convolve2d(mesh, G, mode='same')  # this is the slowest part
t2 = time.time()
# Gaussian addition
mesh_gauss = np.zeros([pixels, pixels])
for n in range(len(I)):
    #g = I[n] * np.exp(-np.log(2) * (((X - Qx[n]) ** 2 + (Y - Qy[n]) ** 2) / (peak_width / 2) ** 2))
    #mesh_gauss += g
    mesh_gauss += I[n] * np.exp(-np.log(2) * (((X - Qx[n]) ** 2 + (Y - Qy[n]) ** 2) / (peak_width / 2) ** 2))
t3 = time.time()



print('Convolve2d took: %s s' % (t2-t1))
print('Gauss addition took: %s s' % (t3-t2))

clim = [0, 10000]

plt.figure(figsize=[16, 16], dpi=60)
plt.subplot(221)
plt.pcolormesh(mesh_all)
plt.axis('image')
plt.title('Pixels')

plt.subplot(222)
plt.pcolormesh(X, Y, mesh)
plt.clim(clim)
plt.axis('image')
plt.title('units')

plt.subplot(223)
plt.pcolormesh(X, Y, mesh_convolve)
plt.clim(clim)
plt.axis('image')
plt.title('convolve2d')

plt.subplot(224)
plt.pcolormesh(X, Y, mesh_gauss)
plt.clim(clim)
plt.axis('image')
plt.title('Gauss addition')

plt.figure()
plt.pcolormesh(X, Y, mesh_gauss - mesh_convolve)
plt.axis('image')

plt.show()