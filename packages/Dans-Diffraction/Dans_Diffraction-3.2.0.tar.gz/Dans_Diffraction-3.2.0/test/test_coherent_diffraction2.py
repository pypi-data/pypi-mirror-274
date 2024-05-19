"""
Test simulating coherent diffraction
"""

import sys, os
import numpy as np
import matplotlib.pyplot as plt # Plotting
from mpl_toolkits.mplot3d import Axes3D
import Dans_Diffraction as dif


# Create ellipsoid of points inside cube
# The ellipsoid is the crystallite, created as lego bricks of unit cells
# the Cube is the new super cell

# max lengths
umax = 50
vmax = 100
wmax = 20
ncells = 2000

choice = np.hstack([np.repeat(0, umax), np.repeat(1, vmax), np.repeat(2, wmax)])
randn = np.random.choice(choice, size=ncells)
randd = np.random.choice([1, -1], size=ncells)

uvw = np.zeros([ncells, 3], dtype=int)
cenuvw = np.array([umax/2, vmax/2, wmax/2], dtype=int)
for i in range(ncells):
    #randn = np.random.choice(choice)
    #randd = np.random.choice([1, -1])
    cenuvw[randn[i]] += randd[i]
    #print(i, 'new cenuvw: ', cenuvw, np.all(uvw == cenuvw, axis=1))
    counter = 1
    while np.any(np.all(uvw == cenuvw, axis=1)):
        #print(counter, cenuvw, i, randn[i], randd[i], np.all(uvw == cenuvw, axis=1))
        cenuvw[randn[i]] += randd[i]
        counter += 1
    #print('store', i, cenuvw, randn[i], counter * randd[i])
    uvw[i, :] = cenuvw

uvw[uvw[:, 0] < 0, 0] += umax
uvw[uvw[:, 0] >= umax, 0] -= umax
uvw[uvw[:, 1] < 0, 1] += vmax
uvw[uvw[:, 1] >= vmax, 1] -= vmax
uvw[uvw[:, 2] < 0, 2] += wmax
uvw[uvw[:, 2] >= wmax, 2] -= wmax

lat_uvw = uvw
old_len = len(lat_uvw)
lat_uvw = np.unique(lat_uvw, axis=0)
new_len = len(lat_uvw)
print('Removed %d identical points' % (old_len - new_len))

dif.fp.newplot3(lat_uvw[:, 0], lat_uvw[:, 1], lat_uvw[:, 2], 'o', ms=3)
ax = plt.gca()
sq = max(umax, vmax, wmax)
#ax.set_xlim([0, umax]); ax.set_ylim([0, vmax]); ax.set_zlim([0, wmax])
ax.set_xlim([0, sq]); ax.set_ylim([0, sq]); ax.set_zlim([0, sq])
plt.show()


xtl = dif.structure_list.Na08CoO2_P63mmc()
uvw, atom_type, label, occ, uiso, mxmymz = xtl.Structure.get()

new_uvw = np.ndarray([0, 3])
new_type = np.ndarray([0])
new_label = np.ndarray([0])
new_occupancy = np.ndarray([0])
new_uiso = np.ndarray([0])
new_mxmymz = np.ndarray([0, 3])

for uval, vval, wval in lat_uvw:
    new_uvw = np.vstack([new_uvw, uvw + [uval, vval, wval]])
    new_type = np.hstack([new_type, atom_type])
    new_label = np.hstack([new_label, label])
    new_occupancy = np.hstack([new_occupancy, occ])
    new_uiso = np.hstack([new_uiso, uiso])
    new_mxmymz = np.vstack([new_mxmymz, mxmymz])

R = xtl.Cell.calculateR(new_uvw)
lp = xtl.Cell.generate_lattice(umax, vmax, wmax)

lat = dif.Crystal()
lat.new_cell(lp)
lat = lat.add_parent(xtl, [[umax, 0, 0], [0, vmax, 0], [0, 0, wmax]])
lat.scale = lat.Parent.scale * len(new_uvw)

uvw2 = lat.Cell.indexR(R)
lat.new_atoms(u=uvw2[:, 0], v=uvw2[:, 1], w=uvw2[:, 2],
              type=new_type, label=new_label, occupancy=new_occupancy, uiso=new_uiso)
print('New cell: %d cells of %d atoms, new atoms: %d' % (ncells,len(uvw), len(new_uvw)))

phkl = [1, 0, 0]
hkl = lat.parenthkl2super(phkl)
pi = xtl.Scatter.new_intensity(phkl)
ii = lat.Scatter.new_intensity(hkl)

print('Parent hkl: %s, intensity: %5.5g' % (phkl, pi))
print('New cell hkl: %s, intensity: %5.5g' % (hkl, ii))


