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
a90 = dif.fc.molecular_attenuation_length('Co', en, 8.9, grazing_angle=90)
a45 = dif.fc.molecular_attenuation_length('Co', en, 8.9, grazing_angle=45)
a10 = dif.fc.molecular_attenuation_length('Co', en, 8.9, grazing_angle=10)
a01 = dif.fc.molecular_attenuation_length('Co', en, 8.9, grazing_angle=1)

# Load files generated online
c90 = np.loadtxt('atten_Co_90.txt')
c45 = np.loadtxt('atten_Co_45.txt')
c10 = np.loadtxt('atten_Co_10.txt')
c01 = np.loadtxt('atten_Co_01.txt')

plt.figure(figsize=[12, 14], dpi=60)
plt.suptitle('Co, Density = 8.9 g cm$^{-1}$', fontsize=20)

plt.subplot(221)
plt.plot(en*1000, a90, '-', lw=3, label='Dans Diffraction')
plt.plot(c90[:, 0], c90[:, 1], ':', lw=2, label='CXRO')
dif.fp.labels('Angle = 90 Deg', 'energy [eV]', 'Attenuation [$\mu$m]', legend=True)

plt.subplot(222)
plt.plot(en*1000, a45, '-', lw=3, label='Dans Diffraction')
plt.plot(c45[:, 0], c45[:, 1], ':', lw=2, label='CXRO')
dif.fp.labels('Angle = 45 Deg', 'energy [eV]', 'Attenuation [$\mu$m]', legend=True)

plt.subplot(223)
plt.plot(en*1000, a10, '-', lw=3, label='Dans Diffraction')
plt.plot(c10[:, 0], c10[:, 1], ':', lw=2, label='CXRO')
dif.fp.labels('Angle = 10 Deg', 'energy [eV]', 'Attenuation [$\mu$m]', legend=True)

plt.subplot(224)
plt.plot(en*1000, a01, '-', lw=3, label='Dans Diffraction')
plt.plot(c01[:, 0], c01[:, 1], ':', lw=2, label='CXRO')
dif.fp.labels('Angle = 1 Deg', 'energy [eV]', 'Attenuation [$\mu$m]', legend=True)

plt.show()
