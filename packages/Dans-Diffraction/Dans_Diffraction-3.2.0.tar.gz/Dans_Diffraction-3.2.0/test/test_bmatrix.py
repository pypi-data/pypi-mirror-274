"""
Check B Matrix from Busing & Levi

Angle Calculations for 3- and 4- Circle X-ray and Neutron Diffraetometers
BY  WILLIAM R.  BUSING AND  HENRI A.  LEVY
Acta  Cryst.  (1967). 22,  457
20/10/2020
"""

import sys, os
import numpy as np

cf = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(cf, '..'))
import Dans_Diffraction as dif
from Dans_Diffraction import fg

fg.nice_print()

#xtl = dif.structure_list.Ca2RuO4()
xtl = dif.structure_list.Na08CoO2_P63mmc()

a, b, c, alpha, beta, gamma = xtl.Cell.lp()

uv = xtl.Cell.UV()
uvs = xtl.Cell.UVstar()
bmatrix = xtl.Cell.Bmatrix()

print('lattice parameters:')
print(a, b, c, alpha, beta, gamma)
print('Unit cell:')
print(uv)
print('Reciprocal unit cell:')
print(uvs)
print('Bmatrix:')
print(bmatrix)

a1, a2, a3 = fg.mag(uv)
alpha3 = fg.ang(uv[0, :], uv[1, :], True)
alpha2 = fg.ang(uv[0, :], uv[2, :], True)
alpha1 = fg.ang(uv[1, :], uv[2, :], True)
print('\nReal space lattice:')
print('a1, a2, a3: %5.3f, %5.3f, %5.3f' % (a1, a2, a3))
print('alpha1, alpha2, alpha3: %5.3f, %5.3f, %5.3f' % (alpha1, alpha2, alpha3))
uvs = uvs / (2 * np.pi)
b1, b2, b3 = fg.mag(uvs)
beta3 = fg.ang(uvs[0, :], uvs[1, :], True)
beta2 = fg.ang(uvs[0, :], uvs[2, :], True)
beta1 = fg.ang(uvs[1, :], uvs[2, :], True)
print('Reciprocal space lattice:')
print('b1, b2, b3: %5.3f, %5.3f, %5.3f' % (b1, b2, b3))
print('beta1, beta2, beta3: %5.3f, %5.3f, %5.3f' % (beta1, beta2, beta3))

B = np.array([[b1, b2 * np.cos(beta3), b3 * np.cos(beta2)],
              [0, b2 * np.sin(beta3), -b3 * np.sin(beta2) * np.cos(alpha1)],
              [0, 0, 1 / a3]])

print('Bmatrix:')
print(B)

h = np.array([[1,0,0], [2,0,0], [1,1,0], [0,0,3], [0,1,3]])
q = xtl.Cell.calculateQ(h)

#qB = 2*np.pi*np.dot(bmatrix, h.T).T
qB = 2*np.pi*np.dot(h, bmatrix.T)

print('\n%20s %20s %20s' % ('(h,k,l)', '(qx, qy, qz)=h.UV*', '(qx, qy, qz)=B.h'))
for n in range(len(h)):
    print('%20s %20s %20s' % (h[n], q[n], qB[n]))