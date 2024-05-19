"""
Compare calculated attenuation length with that of https://henke.lbl.gov/cgi-bin/atten.pl
Co Density 8.9 g ,3^-3
25/1/21
"""

import numpy as np
import matplotlib.pyplot as plt
import Dans_Diffraction as dif

xtl = dif.structure_list.Cobalt()

density = 8.9  # g/cm3
weight = 58.933195  # g
atom_per_volume = 1e-24 * density * dif.fg.Na / weight  # 0.09094331301739197

en = np.arange(0.01, 1, 0.01)

n = dif.fc.xray_refractive_index('Co', en, atom_per_volume)

delta = 1 - np.real(n)
beta = -np.imag(n)
n2 = 1 - delta - 1j*beta

plt.figure(figsize=[12, 10], dpi=60)
plt.plot(en, delta, label='delta')
plt.plot(en, beta, label='Beta')
dif.fp.labels('Co', legend=True)
plt.xscale('log')
plt.yscale('log')
plt.show()


grazing_angle = 2
costh = np.cos(np.deg2rad(grazing_angle))
ki = costh
kt = np.sqrt(n**2 - costh**2)

r = (ki - kt)/(ki + kt)
refl = np.real(r * np.conj(r))

plt.figure(figsize=[12, 10], dpi=60)
plt.plot(en, refl)
plt.show()