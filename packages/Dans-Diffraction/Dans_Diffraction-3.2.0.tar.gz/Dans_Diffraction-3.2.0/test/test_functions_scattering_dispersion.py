"""
Test functions_scattering.pu

"""

import numpy as np
import matplotlib.pyplot as plt
import Dans_Diffraction as dif
from Dans_Diffraction import functions_scattering as fs

#xtl = dif.structure_list.Na08CoO2_P63mmc()

xtl = dif.structure_list.Ca2RuO4()
xtl.Atoms.changeatom(1, mxmymz=[0, 3, 0.3])
xtl.generate_structure()
en = 2.838
hkl = [0, 3, 1]

envals = np.arange(en-0.5, en+0.5, 0.01)
psivals = np.arange(-180, 180)

# uvw, atom_type, label, occ, uiso, mxmymz = xtl.Structure.get()
# q = xtl.Cell.calculateQ(hkl)
# r = xtl.Cell.calculateR(uvw)
# ff = dif.fc.xray_scattering_factor_resonant(atom_type, dif.fg.mag(q), envals)
# refs = fs.autointensity('xray dispersion', q, r, energy_kev=envals, scattering_factor=ff)
refs = xtl.Scatter.new_intensity(hkl, 'xray dispersion', energy_kev=envals)

plt.figure(); plt.plot(envals, refs[0]); plt.title(hkl); plt.xlabel('Energy [keV]')

#refs = fs.autointensity('xray resonant', q, r, psi=psivals)
refs = xtl.Scatter.new_intensity(hkl, 'xray resonant', psi=psivals, energy_kev=en)

plt.figure(); plt.plot(psivals, refs[0]); plt.title(hkl); plt.xlabel('Psi [deg]')

