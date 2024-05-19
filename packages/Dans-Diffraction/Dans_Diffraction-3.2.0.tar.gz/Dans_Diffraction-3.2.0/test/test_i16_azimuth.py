"""
Simulate Azimuthal definition of I16
22/11/2020
"""

import sys, os
import numpy as np
import matplotlib.pyplot as plt # Plotting
from mpl_toolkits.mplot3d import Axes3D  # turn on 3D plotting

sys.path.insert(0, os.path.expanduser('~/Dropbox/Python/Dans_Diffraction'))
import Dans_Diffraction as dif


# Structure
#xtl = dif.structure_list.KCl()
xtl = dif.structure_list.Na08CoO2_P63mmc()

energy_kev = 8.0
hkl = [0, 0, 4]
spectral_hkl = [0, 0, 1]  # hkl parallel to phi axis
azi_hkl = [1, 0, 0]  # azimuthal reference

uvs = xtl.Cell.UVstar()
twotheta = xtl.Cell.tth(hkl, energy_kev)[0]
theta = twotheta / 2

print(xtl.name)
print(xtl.Scatter.hkl(hkl, energy_kev))

# Beamline (lab) coordinate system:
#    z axis : Beam direction
#    x axis : lab horizontal (away from ring)
#    y axis : lab vertical upwards

# Diffractometer coordinate system:
#    z axis : phi axis, parallel to spectral hkl
#    x axis : perpendicular to beam
#    y axis : coaxial with beam

orientation = np.array(dif.fc.orthogonal_axes(xtl.Cell.calculateQ(spectral_hkl), xtl.Cell.calculateQ(azi_hkl)))
orientation = dif.fg.rot3D(orientation, 0, 0, -theta)
print('Orientation matrix:')
print(orientation)
orient_q = np.dot(xtl.Cell.calculateQ(hkl), orientation)
orient_azi = np.dot(xtl.Cell.calculateQ(azi_hkl), orientation)

azi_rad = np.linspace(0, 2 * np.pi, 360)
azi_vec = np.array([np.cos(psi) * orientation[0] + np.sin(psi) * orientation[1] for psi in azi_rad])

sample = [0, 0, 0]
beampipe = [0, 0, 1]
detector_cen = dif.fg.rot3D(beampipe, 0, 0, -twotheta)[0]
q = orient_q[0] #dif.fg.rot3D(orient_q, 0, 0, -theta)[0]
q_azi = orient_azi[0] #dif.fg.rot3D(orient_azi, 0, 0, -theta)[0]

wavevector = 2 * np.pi / dif.fc.energy2wave(energy_kev)
ki = wavevector * dif.fg.norm(beampipe)  # A-1, initial wavevector
kf = wavevector * dif.fg.norm(detector_cen)  # A-1, final wavevector (same magnitude)
q_cen = kf - ki  # A-1, wavevector transfer, centre of detector

# Plot transform: lab_x[0] = x, lab_y[1] = z, lab_z[2] = y

fs = 18

dif.fp.newplot3([0], [0], [0], 'k+')
ax = plt.gca()
dif.fp.plot_arrow([-ki[0], 0], [-ki[2], 0], [-ki[1], 0], col='k', width=4)
dif.fp.plot_arrow([0, kf[0]], [0, kf[2]], [0, kf[1]], col='k', width=4)
dif.fp.plot_arrow([0, q_cen[0]], [0, q_cen[2]], [0, q_cen[1]], col='r', width=4)
ax.plot([q[0]], [q[2]], [q[1]], 'ro', ms=12)
ax.text(q[0], q[2], q[1], 'k$_f$ - k$_i$', fontsize=fs)
ax.text(-ki[0], -ki[2], -ki[1], 'k$_k$', fontsize=fs)
ax.text(kf[0], kf[2], kf[1]+0.2, 'k$_k$', fontsize=fs)

dif.fp.plot_arrow([0, q_azi[0]], [0, q_azi[2]], [0, q_azi[1]], col='grey', width=4)
ax.plot(azi_vec[:, 0], azi_vec[:, 2], azi_vec[:, 1], '-', c='grey', lw=1)
dif.fp.plot_arrow(
    [azi_vec[60, 0], azi_vec[90, 0]],
    [azi_vec[60, 2], azi_vec[90, 2]],
    [azi_vec[60, 1], azi_vec[90, 1]],
    col='grey', width=1
)
ax.text(q_azi[0], q_azi[2], q_azi[1]-0.5, 'azi_ref', fontsize=fs)

dif.fp.labels('I16 Azimuth', 'x', 'z', 'y')

ax.set_xlim([3, -3])
ax.set_ylim([3, -3])
ax.set_zlim([-3, 3])
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.grid(False)
#ax.set_axis_off()
plt.show()
