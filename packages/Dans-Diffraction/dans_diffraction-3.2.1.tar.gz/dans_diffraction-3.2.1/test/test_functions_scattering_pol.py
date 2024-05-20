"""
Test functions_scattering.pu

"""

import numpy as np
import matplotlib.pyplot as plt
import Dans_Diffraction as dif
from Dans_Diffraction import functions_scattering as fs

en = 2.838  # keV
aziref = [0, 1, 0]

xtl = dif.structure_list.Ca2RuO4()
xtl.Atoms.changeatom(1,mxmymz=[0,3,0.3])
xtl.generate_structure()

hkl = [2, 0, 1]
q = xtl.Cell.calculateQ(hkl)
qmag = dif.fg.mag(q)
azirefq = xtl.Cell.calculateQ(aziref)

uvw, at_type, label, occupancy, uiso, mxmymz = xtl.Structure.get()
r = xtl.Cell.calculateR(uvw)
moment = dif.fc.euler_moment(mxmymz, xtl.Cell.UV())
scatlength = dif.fc.neutron_scattering_length(at_type)
ff = dif.fc.xray_scattering_factor(at_type, qmag)
ffmag = dif.fc.magnetic_form_factor(at_type, qmag)
z = dif.fc.element_z(at_type)
dw = dif.fc.debyewaller(uiso, qmag)

xtl.Scatter._use_isotropic_thermal_factor = True
xtl.Scatter._use_magnetic_form_factor = True


def plot_class(xtl, hkl, energy_kev=None, polarisation='sp', azim_zero=(1, 0, 0), psi=0):
    """
    Plots the scattering vectors for a particular azimuth
    :param hkl:
    :param energy_kev:
    :param polarisation:
    :param azim_zero:
    :param psi:
    :return: None
    """

    U1, U2, U3 = xtl.Scatter.scatteringbasis(hkl, azim_zero, psi)
    kin, kout, ein, eout = xtl.Scatter.scatteringvectors(hkl, energy_kev, azim_zero, psi, polarisation)
    print('\nclass')
    print(U1, U2, U3)
    print(kin, kout, ein, eout)

    fig = plt.figure(figsize=[8, 6], dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('x', fontsize=18)
    ax.set_ylabel('y', fontsize=18)
    ax.set_zlabel('z', fontsize=18)
    plt.title('xtl.Scatter (%1.0f,%1.0f,%1.0f) psi=%3.0f' % (hkl[0], hkl[1], hkl[2], psi), fontsize=28)

    ax.plot([0, U1[0]], [0, U1[1]], [0, U1[2]], '-k', lw=2)  # U1
    ax.plot([0, U2[0]], [0, U2[1]], [0, U2[2]], '-k', lw=2)  # U2
    ax.plot([0, U3[0]], [0, U3[1]], [0, U3[2]], '-k', lw=3)  # U3

    ax.plot([-kin[0, 0], 0], [-kin[0, 1], 0], [-kin[0, 2], 0], '-b')  # Kin
    ax.plot([0, kout[0, 0]], [0, kout[0, 1]], [0, kout[0, 2]], '-b')  # Kout

    ax.plot([-kin[0, 0], -kin[0, 0] + ein[0, 0]],
            [-kin[0, 1], -kin[0, 1] + ein[0, 1]],
            [-kin[0, 2], -kin[0, 2] + ein[0, 2]], '-g')  # ein
    ax.plot([kout[0, 0], kout[0, 0] + eout[0, 0]],
            [kout[0, 1], kout[0, 1] + eout[0, 1]],
            [kout[0, 2], kout[0, 2] + eout[0, 2]], '-g')  # eout

    # ax.plot([0, a[0]], [0, a[1]], [0, a[2]], '-m')  # a
    # ax.plot([0, b[0]], [0, b[1]], [0, b[2]], '-m')  # b
    # ax.plot([0, c[0]], [0, c[1]], [0, c[2]], '-m')  # c

    # Add moment manually after
    # ax.plot([0, moment[0, 0]], [0, moment[0, 1]], [0, moment[0, 2]], '-r', lw=2)  # moment


def plot_fun(q, energy_kev=None, polarisation='sp', azi_ref_q=(1, 0, 0), psi=0):
    U1, U2, U3 = fs.scatteringbasis(q, azi_ref_q, psi)
    kin, kout, ein, eout = fs.scatteringvectors(q, energy_kev, azi_ref_q, psi, polarisation)

    print('\nfun')
    print(U1, U2, U3)
    print(kin, kout, ein, eout)

    fig = plt.figure(figsize=[8, 6], dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('x', fontsize=18)
    ax.set_ylabel('y', fontsize=18)
    ax.set_zlabel('z', fontsize=18)
    plt.title('functions_scattering (%1.0f,%1.0f,%1.0f) psi=%3.0f' % (hkl[0], hkl[1], hkl[2], psi), fontsize=28)

    ax.plot([0, U1[0]], [0, U1[1]], [0, U1[2]], '-k', lw=2)  # U1
    ax.plot([0, U2[0]], [0, U2[1]], [0, U2[2]], '-k', lw=2)  # U2
    ax.plot([0, U3[0]], [0, U3[1]], [0, U3[2]], '-k', lw=3)  # U3

    ax.plot([-kin[0, 0], 0], [-kin[0, 1], 0], [-kin[0, 2], 0], '-b')  # Kin
    ax.plot([0, kout[0, 0]], [0, kout[0, 1]], [0, kout[0, 2]], '-b')  # Kout

    ax.plot([-kin[0, 0], -kin[0, 0] + ein[0, 0]],
            [-kin[0, 1], -kin[0, 1] + ein[0, 1]],
            [-kin[0, 2], -kin[0, 2] + ein[0, 2]], '-g')  # ein
    ax.plot([kout[0, 0], kout[0, 0] + eout[0, 0]],
            [kout[0, 1], kout[0, 1] + eout[0, 1]],
            [kout[0, 2], kout[0, 2] + eout[0, 2]], '-g')  # eout

    # ax.plot([0, a[0]], [0, a[1]], [0, a[2]], '-m')  # a
    # ax.plot([0, b[0]], [0, b[1]], [0, b[2]], '-m')  # b
    # ax.plot([0, c[0]], [0, c[1]], [0, c[2]], '-m')  # c

    # Add moment manually after
    # ax.plot([0, moment[0, 0]], [0, moment[0, 1]], [0, moment[0, 2]], '-r', lw=2)  # moment


plot_class(xtl, hkl, en, polarisation='sp', azim_zero=aziref, psi=-90)
plot_fun(q, en, polarisation='sp', azi_ref_q=azirefq, psi=-90)