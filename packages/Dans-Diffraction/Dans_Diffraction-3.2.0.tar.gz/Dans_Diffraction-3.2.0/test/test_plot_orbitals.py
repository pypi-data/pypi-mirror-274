"""
Plot orbitals using spherical harmonics
based on code python/spherical_harmonics.py
22/11/2020
"""

import sys,os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm

sys.path.insert(0, os.path.expanduser('~/Dropbox/Python/Dans_Diffraction'))
import Dans_Diffraction as dif


def sph2cart(theta, phi, r):
    """
    From https://en.wikipedia.org/wiki/Spherical_coordinate_system
    Maths convention, theta+phi swapped compared with physics iso convention,
    see https://en.wikipedia.org/wiki/Spherical_coordinate_system
    :param theta: azimuth (radians)
    :param phi: inclination (radians)
    :param r: radius
    :return: x, y, z
    """
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    return x, y, z


def generate_orbital(l=2, n=0, size=1.0, vertical=(0,0,1), horizontal=(1,0,0), nbits=100):
    """

    :param l:
    :param n:
    :param size:
    :param vertical:
    :param horizontal:
    :param nbits:
    :return: x, y, z
    """
    angles = np.linspace(-np.pi, np.pi, nbits)
    theta, phi = np.meshgrid(angles, angles)

    # Generate Real Spherical Harmonics / atomic orbitals
    # https://en.wikipedia.org/wiki/Table_of_spherical_harmonics#Real_spherical_harmonics
    rt2 = 1 / np.sqrt(2)
    it2 = 1j / np.sqrt(2)
    if l == 0:
        sph = sph_harm(0, 0, theta, phi)  # s, Y00
    elif l == 1:
        Y1m1 = sph_harm(-1, 1, theta, phi)
        Y11 = sph_harm(1, 1, theta, phi)
        if n == -1:
            sph = it2 * (Y11 + Y1m1)  # py, Y1-1
        elif n == 0:
            sph = sph_harm(0, 1, theta, phi)  # pz, Y10
        elif n == 1:
            sph = rt2 * (Y1m1 - Y11)  # px, Y11
        else:
            raise Exception('n must be -l-l')
    elif l == 2:
        Y2m2 = sph_harm(-2, 2, theta, phi)
        Y2m1 = sph_harm(-1, 2, theta, phi)
        Y21 = sph_harm(1, 2, theta, phi)
        Y22 = sph_harm(2, 2, theta, phi)
        if n == -2:
            sph = it2 * (Y2m2 - Y22)  # dxy, Y2-2
        elif n == -1:
            sph = it2 * (Y2m1 + Y21)  # dyz, Y2-1
        elif n == 0:
            sph = sph_harm(0, 2, theta, phi)  # d3z^2-r^2, Y20
        elif n == 1:
            sph = rt2 * (Y2m1 - Y21)  # dxz, Y21
        elif n == 2:
            sph = rt2 * (Y22 + Y2m2)  # dx^2-y^2, Y22
        else:
            raise Exception('n must be -l-l')
    else:
        raise Exception('l > 2 not implemented yet')

    r = np.real(sph * np.conj(sph))  # this one is correct compared to images on google
    r = r * size / np.max(r)

    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    # Coordinate system
    zaxis, xaxis, yaxis = dif.fc.orthogonal_axes(vertical, horizontal)
    x_coord = x * xaxis[0] + y * yaxis[0] + z * zaxis[0]
    y_coord = x * xaxis[1] + y * yaxis[1] + z * zaxis[1]
    z_coord = x * xaxis[2] + y * yaxis[2] + z * zaxis[2]
    return x_coord, y_coord, z_coord


def symmetry_orbital(sym_op, x, y, z):
    """

    :param sym_op:
    :param x:
    :param y:
    :param z:
    :return:
    """
    sym = sym_op.lower()
    sym = sym.replace('/', './')
    sym = sym.strip('\"\'')
    sym = sym.replace('mx', 'x').replace('my', 'y').replace('mz', 'z')
    x, y, z = eval(sym)
    return x, y, z


xtl = dif.structure_list.Ca2RuO4()
xyz, ats = xtl.Properties.atomic_neighbours(11)
xval, yval, zval = generate_orbital(l=2, n=0, size=1, vertical=xyz[-1], horizontal=xyz[1], nbits=50)
shape = np.shape(xval)
uvw = xtl.Cell.indexR([xval.reshape(-1), yval.reshape(-1), zval.reshape(-1)])
xsym = uvw[:, 0].reshape(shape)
ysym = uvw[:, 1].reshape(shape)
zsym = uvw[:, 2].reshape(shape)

fig = plt.figure()
ax = fig.gca(projection='3d')
for symop in ['x,y,z']: #xtl.Symmetry.symmetry_operations:
    sx, sy, sz = symmetry_orbital(symop, xval, yval, zval)
    xxx = xtl.Cell.calculateR([sx.reshape(-1), sy.reshape(-1), sz.reshape(-1)])
    sx = xxx[:, 0].reshape(shape)
    sy = xxx[:, 1].reshape(shape)
    sz = xxx[:, 2].reshape(shape)
    ax.plot_surface(sx, sy, sz, cmap=plt.get_cmap('hot'), linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.set_xlim3d(-0.5, 0.5)
ax.set_ylim3d(-0.5, 0.5)
ax.set_zlim3d(-0.5, 0.5)

plt.show()
