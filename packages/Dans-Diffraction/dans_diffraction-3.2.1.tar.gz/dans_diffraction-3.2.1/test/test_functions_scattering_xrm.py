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

#hkl = xtl.Cell.all_hkl(en, 120)
hkl = [1, 1, 0]
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

psivals = np.arange(-180, 181, 2)
inten = {
    'class_xray_nonresonant_magnetic': [xtl.Scatter.xray_nonresonant_magnetic(hkl, energy_kev=en, azim_zero=aziref, psi=psi) for psi in psivals],
    'class_xray_resonant': xtl.Scatter.xray_resonant(hkl, energy_kev=en, polarisation='sp', F0=0, F1=1, F2=0, azim_zero=aziref, PSI=psivals).reshape(-1),
    'class_xray_resonant_magnetic': [xtl.Scatter.xray_resonant_magnetic(hkl, energy_kev=en, F0=0, F1=1, F2=0, polarisation='sp', azim_zero=aziref, psi=psi) for psi in psivals],
    'fun_xray_nonresonant_magnetic': [fs.intensity((fs.sf_magnetic_xray_beamline(q, r, occupancy, moment, en, ffmag, dw, azi_ref_q=azirefq, psi=psi, polarisation='s-p'))) for psi in psivals],
    'fun_xray_resonant': [fs.intensity(fs.sf_magnetic_xray_resonant(q, r, occupancy, moment, en, debyewaller=dw, polarisation='sp', azi_ref_q=azirefq, psi=psi, f0=0, f1=1, f2=0)) for psi in psivals],
    'fun_xray_resonant_magnetic': [fs.intensity(fs.sf_xray_resonant_magnetic(q, r, occupancy, moment, en, debyewaller=dw, azi_ref_q=azirefq, psi=psi, polarisation='s-p', f0=0, f1=1, f2=0)) for psi in psivals]
}
keys = ['class_xray_nonresonant_magnetic',
        'class_xray_resonant',
        'class_xray_resonant_magnetic',
        'fun_xray_nonresonant_magnetic',
        'fun_xray_resonant',
        'fun_xray_resonant_magnetic']
cols = {
    'class_xray_nonresonant_magnetic': 'b-',
    'class_xray_resonant': 'g-',
    'class_xray_resonant_magnetic': 'r-',
    'fun_xray_nonresonant_magnetic': 'c:',
    'fun_xray_resonant': 'y--',
    'fun_xray_resonant_magnetic': 'm:'
}

plt.figure(figsize=[12, 10], dpi=60)
for key in ['class_xray_nonresonant_magnetic', 'class_xray_resonant', 'class_xray_resonant_magnetic']:
    plt.plot(psivals, inten[key], cols[key], lw=3, label=key)
for key in ['fun_xray_nonresonant_magnetic', 'fun_xray_resonant', 'fun_xray_resonant_magnetic']:
    plt.plot(psivals, inten[key], cols[key], lw=2, label=key)
plt.xlabel('psi')
plt.title('E = %1.4f keV hkl = (%1.0f,%1.0f,%1.0f)' % (en, hkl[0], hkl[1], hkl[2]), fontsize=20)
plt.legend(loc=0, frameon=False)
plt.show()
