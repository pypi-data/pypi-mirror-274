"""
Test simulating laue backscattering
"""

import sys, os
import numpy as np
import matplotlib.pyplot as plt # Plotting
from mpl_toolkits.mplot3d import Axes3D
import time
import Dans_Diffraction as dif

xtl = dif.structure_list.LiCoO2()

xtl.Cell.orientation.rotate_6circle(chi=0, phi=0)

erange = np.arange(20, 80, 5)
detector_distance = 0.05  # 5 cm
detector_radius = 0.15 / 2  # 150 mm
hole_radius = 0.01  # 1 cm
min_tth = 180 - np.rad2deg(np.arctan(detector_radius / detector_distance))
max_tth = 180 - np.rad2deg(np.arctan(hole_radius / detector_distance))
print(min_tth, max_tth)

hkl = xtl.Cell.all_hkl(erange[-1], max_tth)
print(len(hkl))
qlab = xtl.Cell.calculateQ(hkl)
qmag = dif.fg.mag(qlab)
qang = np.rad2deg(np.arccos(np.dot(dif.fg.norm(qlab), [0, 0, 1])))
qdet = (qang < np.rad2deg(np.arctan(detector_radius / detector_distance))) * (qmag < 50)

hkl = hkl[qdet, :]
inten = xtl.Scatter.intensity(hkl)
qx = qlab[qdet, 0]
qy = qlab[qdet, 1]
qmag = dif.fg.mag(qlab[qdet, :2])
print(len(hkl))

irat = inten > 0.01
hkl = hkl[irat, :]
inten = inten[irat]
qx = qx[irat]
qy = qy[irat]
qmag = qmag[irat]
print(len(hkl))

q_max = 8
pixels = 1001  # reduce this to make convolution faster
pixel_size = (2.0*q_max)/pixels
mesh = np.zeros([pixels, pixels])
mesh_x = np.linspace(-q_max, q_max, pixels)
xx, yy = np.meshgrid(mesh_x, mesh_x)
peak_width = 0.05

for en in erange:
    en_tth = xtl.Cell.tth(hkl, en)
    #kf = qlab + [0, 0, -dif.fc.wavevector(en)] # == qlab[:, 0], qlab[:, 1]
    idx = (en_tth > min_tth) * (en_tth < max_tth) * (qmag < q_max)
    print(en, np.sum(idx))
    en_inten = inten[idx]
    en_qx = qx[idx]
    en_qy = qy[idx]
    for n in range(len(en_inten)):
        # Add each reflection as a gaussian
        mesh += en_inten[n] * np.exp(-np.log(2) * (((xx - en_qx[n]) ** 2 + (yy - en_qy[n]) ** 2) / (peak_width / 2) ** 2))

background = 0
plt.figure(figsize=[12, 10], dpi=80)
cmap = plt.get_cmap('hot_r')
plt.pcolormesh(xx, yy, mesh, cmap=cmap)
plt.axis('image')
plt.colorbar()
plt.clim([background - (np.max(mesh) / 200), background + (np.max(mesh) / 50)])

"""
for en in erange:
    en_tth = xtl.Cell.tth(hkl, en)
    #kf = qlab + [0, 0, -dif.fc.wavevector(en)] # == qlab[:, 0], qlab[:, 1]
    idx = (en_tth > min_tth) * (en_tth < max_tth) * (qmag < q_max)
    #print(en, np.sum(idx))
    en_inten = inten[idx]
    en_qx = qx[idx]
    en_qy = qy[idx]
    plt.plot(en_qx, en_qy, 'x', ms=6, label=en)
plt.legend(loc=0)
"""
