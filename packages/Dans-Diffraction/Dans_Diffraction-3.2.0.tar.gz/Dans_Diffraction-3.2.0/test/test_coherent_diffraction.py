"""
Test simulating coherent diffraction
"""

import sys, os
import numpy as np
import matplotlib.pyplot as plt # Plotting
from mpl_toolkits.mplot3d import Axes3D
import time
import Dans_Diffraction as dif


xtl = dif.structure_list.Na08CoO2_P63mmc()
#xtl = dif.structure_list.Ca2RuO4()

# max lengths
# Box size in unit cells
umax = 300
vmax = 90
wmax = 30
# crysalite size in unit cells
uwid = umax/10
vwid = vmax/10
wwid = wmax/10
# number of cells to add
ncells = 500
# reflection image npixels
npixel_length = 100
# Parent hkl
phkl = [2, 0, 0]

"""
# Method 1: Create ellipsoid of points inside cube
# The ellipsoid is the crystallite, created as lego bricks of unit cells
# the Cube is the new super cell
ua = np.random.normal(loc=umax/2, scale=uwid, size=(ncells, 1)).astype(int)
va = np.random.normal(loc=vmax/2, scale=vwid, size=(ncells, 1)).astype(int)
wa = np.random.normal(loc=wmax/2, scale=wwid, size=(ncells, 1)).astype(int)
lat_uvw = np.hstack([ua, va, wa])
"""
# Alternative method - build connected cells
choice = np.hstack([np.repeat(0, umax), np.repeat(1, vmax), np.repeat(2, wmax)])
randn = np.random.choice(choice, size=ncells)
randd = np.random.choice([1, -1], size=ncells)
lat_uvw = np.zeros([ncells, 3], dtype=int)
cenuvw = np.array([umax/2, vmax/2, wmax/2], dtype=int)
lat_uvw[0, :] = cenuvw
for i in range(1, ncells):
    #randn = np.random.choice(choice)
    #randd = np.random.choice([1, -1])
    cenuvw[randn[i]] += randd[i]
    #print(i, 'new cenuvw: ', cenuvw, np.all(lat_uvw == cenuvw, axis=1))
    counter = 1
    while np.any(np.all(lat_uvw == cenuvw, axis=1)):
        #print(counter, cenuvw, i, randn[i], randd[i], np.all(lat_uvw == cenuvw, axis=1))
        cenuvw[randn[i]] += randd[i]
        counter += 1
    #print('store', i, cenuvw, randn[i], counter * randd[i])
    lat_uvw[i, :] = cenuvw

# Put all points into the cell
lat_uvw[lat_uvw[:, 0] < 0, 0] += umax
lat_uvw[lat_uvw[:, 0] >= umax, 0] -= umax
lat_uvw[lat_uvw[:, 1] < 0, 1] += vmax
lat_uvw[lat_uvw[:, 1] >= vmax, 1] -= vmax
lat_uvw[lat_uvw[:, 2] < 0, 2] += wmax
lat_uvw[lat_uvw[:, 2] >= wmax, 2] -= wmax
# Remove identical points
old_len = len(lat_uvw)
lat_uvw = np.unique(lat_uvw, axis=0)
new_len = len(lat_uvw)
print('Removed %d identical points' % (old_len - new_len))

# 3D plot of points in real space
lat_r = xtl.Cell.calculateR(lat_uvw)
avu = np.mean(lat_uvw, axis=0)
avr = np.mean(lat_r, axis=0)
print('Average position: uvw=(%1.0f,%1.0f,%1.0f), xyz=(%5.2f,%5.2f,%5.2f)' % (avu[0], avu[1], avu[2], avr[0], avr[1], avr[2]))

dif.fp.newplot3(lat_r[:, 0], lat_r[:, 1], lat_r[:, 2], 'o', ms=3)
dif.fp.plot_cell(xtl.Cell.calculateR([umax/2, vmax/2, wmax/2]), xtl.Cell.calculateR([[umax, 0, 0], [0, vmax, 0], [0, 0, wmax]]))
ax = plt.gca()
#lp = xtl.Cell.lp()
#sq = max(umax*lp[0], vmax*lp[1], wmax*lp[2])
sq = np.max(lat_r)
#ax.set_xlim([0, umax]); ax.set_ylim([0, vmax]); ax.set_zlim([0, wmax])
#ax.set_xlim([0, sq]); ax.set_ylim([0, sq]); ax.set_zlim([0, sq])
ax.set_xlabel('X [A]')
ax.set_ylabel('Y [A]')
ax.set_zlabel('Z [A]')
plt.show()

dif.fp.newplot3(lat_uvw[:, 0], lat_uvw[:, 1], lat_uvw[:, 2], 'o', ms=3)
dif.fp.plot_cell([umax/2, vmax/2, wmax/2], [[umax, 0, 0], [0, vmax, 0], [0, 0, wmax]])
ax = plt.gca()
ax.set_xlabel('U [rlu]')
ax.set_ylabel('V [rlu]')
ax.set_zlabel('W [rlu]')
plt.show()

# BUild super cell
uvw, atom_type, label, occ, uiso, mxmymz = xtl.Structure.get()
natoms = len(uvw)
tot_len = new_len * len(uvw)
new_uvw = np.zeros([tot_len, 3])
new_type = np.empty(tot_len, dtype='<U2')
new_label = np.empty(tot_len, dtype='<U5')
new_occupancy = np.zeros([tot_len])
new_uiso = np.zeros([tot_len])
new_mxmymz = np.zeros([tot_len, 3])
print('Building lattice')
for n, (uval, vval, wval) in enumerate(lat_uvw):
    new_uvw[n*natoms:(n+1)*natoms, :] = uvw + [uval, vval, wval]
    new_type[n*natoms:(n+1)*natoms] = atom_type
    new_label[n*natoms:(n+1)*natoms] = label
    new_occupancy[n*natoms:(n+1)*natoms] = occ
    new_uiso[n*natoms:(n+1)*natoms] = uiso
    new_mxmymz[n*natoms:(n+1)*natoms, :] = mxmymz

R = xtl.Cell.calculateR(new_uvw)
lp = xtl.Cell.generate_lattice(umax, vmax, wmax)

print('Creating cystallite supercell')
lat = dif.Crystal()
lat.name = xtl.name + ' Crystallite'
lat.new_cell(lp)
print('add atoms')
lat = lat.add_parent(xtl, [[umax, 0, 0], [0, vmax, 0], [0, 0, wmax]])
lat.scale = lat.Parent.scale * len(new_uvw)
print('scale: %s' % lat.scale)
uvw2 = lat.Cell.indexR(R)
lat.new_atoms(u=uvw2[:, 0], v=uvw2[:, 1], w=uvw2[:, 2],
              type=new_type, label=new_label, occupancy=new_occupancy, uiso=new_uiso)
print('New cell: %d cells of %d atoms, new atoms: %d' % (ncells,len(uvw), len(new_uvw)))

hkl = lat.parenthkl2super(phkl)
print('calculate intensities')
pi = xtl.Scatter.new_intensity(phkl)
ii = lat.Scatter.new_intensity(hkl)

print('Parent hkl: %s, intensity: %5.5g' % (phkl, pi))
print('New cell hkl: %s, intensity: %5.5g' % (hkl, ii))

pixel_range = np.arange(-npixel_length/2, npixel_length/2+1)
px, py = np.meshgrid(pixel_range, pixel_range)
dpx = np.vstack([px.reshape(-1), py.reshape(-1), np.zeros(px.size)]).T

pxhkl = dpx + hkl[0, :]
#pxhkl = np.zeros([len(dpx), 3])
#for n in range(len(dpx)):
#    pxhkl[n, :] = [hkl[0, 0] + dpx[n, 0], hkl[0, 1] + dpx[n, 1], hkl[0, 2] + dpx]

print('Calculate pixel intensity')
ii = lat.Scatter.new_intensity(pxhkl)
ii = ii.reshape(px.shape)

q = lat.Cell.calculateQ(pxhkl)
qx, qy, qz = q[:, 0], q[:, 1], q[:, 2]
qx = qx.reshape(px.shape)
qy = qy.reshape(px.shape)
qz = qz.reshape(px.shape)

mi, mj = np.unravel_index(np.argmax(ii), ii.shape)
print('Max Qpixel intensity Q(%d,%d) = %5.2f' % (mi, mj, np.max(ii)))

plt.figure(figsize=[20, 6], dpi=60)
plt.suptitle(lat.name, fontsize=20)
plt.subplots_adjust(wspace=0.3)
plt.subplot(131)
plt.pcolormesh(qx, qy, ii)
plt.clim([0, np.max(ii)/10])
dif.fp.labels(None, 'Qx', 'Qy')

plt.subplot(132)
plt.plot(qx[mi, :], ii.sum(axis=1) / ii.shape[1])
plt.plot(qx[mi, :], ii[mi, :])
dif.fp.labels(None, 'Qx')
plt.yscale('log')

plt.subplot(133)
plt.plot(qy[:, mj], ii.sum(axis=0) / ii.shape[0])
plt.plot(qy[:, mj], ii[:, mj])
dif.fp.labels(None, 'Qy')
plt.yscale('log')

plt.show()

