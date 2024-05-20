"""
Test alternative x-ray scattering factors as used by VESTA
Uses the coefficients for analytical approximation to the scattering factors from:
       "Waasmaier and Kirfel, Acta Cryst. (1995) A51, 416-431"
    File from https://github.com/diffpy/libdiffpy/blob/master/src/runtime/f0_WaasKirf.dat

Result - almost no difference between scattering factor calculations, generally on the order of 1e-4

9/6/2021
"""

import numpy as np
import matplotlib.pyplot as plt

import Dans_Diffraction as dif

elements = ['Co', 'Ti', 'O', 'U']
qmag = np.arange(0, 4, 0.01)

scatfac_itc = dif.functions_crystallography.xray_scattering_factor(elements, qmag)  # International tables
scatfac_wsk = dif.functions_crystallography.xray_scattering_factor_WaasKirf(elements, qmag)  # WaasKirf
"""
for n in range(len(elements)):
    plt.figure(figsize=[8, 10], dpi=60)
    plt.subplots_adjust(hspace=0.3)
    plt.subplot(211)
    plt.plot(qmag, scatfac_itc[:, n], '-', lw=4, label='ITC')
    plt.plot(qmag, scatfac_wsk[:, n], '-', lw=2, label='WaasKirf')
    dif.fp.labels(elements[n], 'Q [A-1]', 'FF', legend=True)

    plt.subplot(212)
    plt.plot(qmag, scatfac_itc[:, n] - scatfac_wsk[:, n], '-', lw=4, label='Difference')
    dif.fp.labels(elements[n], 'Q [A-1]', 'Difference')
"""

# Test x-ray Intensities
xtl = dif.Crystal()
xtl.name = 'Trial'
xtl.Cell.latt([2.86, 2.86, 2.86, 90, 90, 90])
xtl.Atoms(u=[0], v=[0], w=[0], type='Fe', label='Fe1', occupancy=1.0, uiso=0.0126651)  # B = 1.0
#xtl.Atoms(u=[0], v=[0], w=[0], type='Fe', label='Fe1', occupancy=1.0, uiso=0.001)
#xtl.Atoms(u=[0], v=[0], w=[0], type='Fe', label='Fe1', occupancy=1.0, uiso=0.0)
xtl.Symmetry.load_spacegroup(1)  # P1
xtl.generate_structure()
xtl.write_cif('trial_structure.cif', 'a simple cubic structure with 1 atom and no symmetry')

hkl = [[1, 0, 0], [1, 1, 0], [1, 1, 1], [2, 0, 0], [2, 1, 0], [2, 1, 1]]
energy = dif.fg.Cu
tth = xtl.Cell.tth(hkl, energy)
i_itc = xtl.Scatter.x_ray(hkl)
i_wsk = xtl.Scatter._x_ray_WaasKirf(hkl)

# Vesta intensities
"""
with Uiso set to 0.126651
 h    k    l      d (Å)      F(real)      F(imag)          |F|         2θ          I    M
   1    0    0   2.860000    20.879536     0.000000      20.3      31.24933  100.00000    1
   1    1    0   2.022325    18.362156     0.000000      17.3569   44.77844    33.0789    1
   1    1    1   1.651222    16.534076     0.000000      15.1951   55.61480    15.4951    1
   2    0    0   1.430000    15.091034     0.000000      13.4839   65.18614     8.5671    1
   2    1    0   1.279031    13.914633     0.000000      12.0877   74.06244     5.3150    1
   2    1    1   1.167590    12.935283     0.000000      10.9250   82.55886     3.6339    1

with Uiso set to 0.001
 h    k    l      d (Å)      F(real)      F(imag)          |F|         2θ          I    M
   1    0    0   2.860000    20.879536     0.000000      20.8795   31.24933  100.00000    1
   1    1    0   2.022325    18.362156     0.000000      18.3622   44.77844   34.99468    1
   1    1    1   1.651222    16.534076     0.000000      16.5341   55.61480   17.34185    1
   2    0    0   1.430000    15.091034     0.000000       15.091   65.18614   10.14355    1
   2    1    0   1.279031    13.914633     0.000000      13.9146   74.06244    6.65749    1
   2    1    1   1.167590    12.935283     0.000000      12.9353   82.55886    4.81540    1

with Uiso set to zero:
 h    k    l      d (Å)      F(real)      F(imag)          |F|         2θ          I    M
   1    0    0   2.860000    20.929984     0.000000        20.93   31.24933  100.00000    1
   1    1    0   2.022325    18.450994     0.000000       18.451   44.77844   35.16399    1
   1    1    1   1.651222    16.654212     0.000000      16.6542   55.61480   17.51006    1
   2    0    0   1.430000    15.237412     0.000000      15.2374   65.18614   10.29149    1
   2    1    0   1.279031    14.083546     0.000000      14.0835   74.06244    6.78727    1
   2    1    1   1.167590    13.123940     0.000000      13.1239   82.55886    4.93302    1
"""
vesta_int = np.array([20.3, 17.3569, 15.1951, 13.4839, 12.0877, 10.9250]) ** 2  # U=0.126651
#vesta_int = np.array([20.8795, 18.3622, 16.5341, 15.091, 13.9146, 12.9353]) ** 2  # U=0.001
#vesta_int = np.array([20.93, 18.451, 16.6542, 15.2374, 14.0835, 13.1239]) ** 2  # Uiso=0

# CrystalDiffract
"""
    h   k   l   d                   2th                 Intensity               I/Imax                  m   N   Lp
    1	0	0	2.86	            31.2473974697661	0.29042831419888	    1	                    2	1	6.19490855862252
    1	1	0	2.02232539419402	44.7755902527989	0.000819267107205278	0.00282089268556735	    2	2	2.80308181405097
    1	1	1	1.65122176988313	55.6111583673064	3.27099591503281E-06	1.12626619207413E-05	2	3	1.71324287405888
    2	0	0	1.43	            65.1817167489989	1.54002692047396E-08	5.30260599667074E-08	2	4	1.20291222015685
    2   1	0	1.27903088313013	74.0572235020635	8.1345863811833E-11	    2.80089302023524E-10	2	5	0.928630159425195
    2	1	1	1.16759011072712	82.5527932754825	4.73666509032186E-13	1.63092400387597E-12	2	6	0.777218154731114
    
With APDs turned off
    1	0	0	2.86	            31.2473974697661	36.2358852520877	1	                2	1	6.19490855862252
    1	1	0	2.02232539419402	44.7755902527989	12.7533818219843	0.351954470913595	2	2	2.80308181405097
    1	1	1	1.65122176988313	55.6111583673064	6.35301333563422	0.175323806537007	2	3	1.71324287405888
    2	0	0	1.43	            65.1817167489989	3.73188282837793	0.102988592728335	2	4	1.20291222015685
    2	1	0	1.27903088313013	74.0572235020635	2.45943349828726	0.0678728691510457	2	5	0.928630159425195
    2	1	1	1.16759011072712	82.5527932754825	1.78678463450855	0.0493098104842245	2	6	0.777218154731114
"""
Lp = np.array([6.19490855862252, 2.80308181405097, 1.71324287405888, 1.20291222015685,
               0.928630159425195, 0.777218154731114])
cd_int = np.array([0.29042831419888, 0.000819267107205278, 3.27099591503281E-06, 1.54002692047396E-08,
                   8.1345863811833E-11, 4.73666509032186E-13])
cd_int = np.array([36.2358852520877, 12.7533818219843, 6.35301333563422, 3.73188282837793,  # with APDs turned off
                   2.45943349828726, 1.78678463450855]) ** 2 / Lp**2

# CCTBX, Federica's Crystal.py
"""
# APD 0.0126651
(h,k,l)        d_spacing (A)       TwoTheta (deg)      bragg
(1, 0, 0)      2.8600000000000003  31.24862781454893   412.08850264923274
(1, 1, 0)      2.022325394193526   44.777402532965155  301.2624052458135
(1, 1, 1)      1.6512217698823302  55.613478555631964  230.89059694320247
(2, 0, 0)      1.4300000000000002  65.18452942240874   181.81645091888328
(1, 2, 0)      1.2790308831298798  74.06054229551098   146.11253224973674
(2, 1, 1)      1.1675901107266484  82.55665523634654   119.35609757553435
"""
cctbx_int = np.array([412.08850264923274, 301.2624052458135, 230.89059694320247, 181.81645091888328,
                      146.11253224973674, 119.35609757553435])

# Mercury
"""
     h      k      l  d-spacing       F^2     multiplicity
     1      0      0      2.86      411.849        2
     1      1      0   2.02233      301.353        2
     1      1      1   1.65122      231.047        2
     2      0      0      1.43      181.839        2
     2      1      0   1.27903      146.028        2
     2      1      1   1.16759      119.241        2
"""
mercury_int = np.array([411.849, 301.353, 231.047, 181.839, 146.028, 119.241])

print('X-Ray Intensities')
print('Energy = %6.4f keV, wl = %6.4f A' % (energy, dif.fc.energy2wave(energy)))
print(' (h,k,l)    two-theta   Intensity1 Intensity2  Vesta  CrystalDiffract  CCTBX  Mercury')
for n in range(len(hkl)):
    print('%10s %8.4f %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f' % (hkl[n], tth[n], i_itc[n], i_wsk[n], vesta_int[n],
                                                                    cd_int[n], cctbx_int[n], mercury_int[n]))

"""
X-Ray Intensities with Uiso = 0.001
Energy = 8.0480 keV, wl = 1.5406 A
 (h,k,l)    two-theta   Intensity1 Intensity2  Vesta 
 [1, 0, 0]  31.2487     436.85     437.10     435.95
 [1, 1, 0]  44.7775     339.49     339.38     337.17
 [1, 1, 1]  55.6136     276.50     276.31     273.38
 [2, 0, 0]  65.1847     231.19     231.16     227.74
 [2, 1, 0]  74.0607     197.26     197.37     193.62
 [2, 1, 1]  82.5568     171.15     171.31     167.32
 
 X-Ray Intensities with Uiso = 1e-10
Energy = 8.0480 keV, wl = 1.5406 A
 (h,k,l)    two-theta   Intensity1 Intensity2  Vesta
 [1, 0, 0]  31.2487     437.81     438.06     438.06
 [1, 1, 0]  44.7775     340.54     340.44     340.44
 [1, 1, 1]  55.6136     277.55     277.36     277.36
 [2, 0, 0]  65.1847     232.21     232.18     232.18
 [2, 1, 0]  74.0607     198.23     198.35     198.34
 [2, 1, 1]  82.5568     172.07     172.24     172.24
 """
