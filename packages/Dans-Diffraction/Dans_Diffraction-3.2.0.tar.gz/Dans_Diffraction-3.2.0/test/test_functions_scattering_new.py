"""
Test functions_scattering.pu

"""

import numpy as np
import matplotlib.pyplot as plt
import Dans_Diffraction as dif
from Dans_Diffraction import functions_scattering as fs

en = 2.838  # keV
aziref = [1, 1, 0]

xtl = dif.structure_list.Ca2RuO4()
xtl.Atoms.changeatom(1,mxmymz=[0,3,0.3])
xtl.generate_structure()

hkl = xtl.Cell.all_hkl(en, 120)
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

kwargs={
    'occ': occupancy,
    'debyewaller': dif.fc.debyewaller(uiso),
    'scattering_factor': ff,
    'moment': moment,

}
ii = fs.autointensity('xray', q, r, **kwargs)

print(ii)
"""
class_inten = {
    'neutron': xtl.Scatter.neutron(hkl),
    'xray': xtl.Scatter.x_ray(hkl),
    'xfast': xtl.Scatter.x_ray_fast(hkl),
    'neutron_magnetic': xtl.Scatter.magnetic_neutron(hkl),
    'xray_magnetic': xtl.Scatter.xray_magnetic(hkl),
    'xray_nonresonant_magnetic': xtl.Scatter.xray_nonresonant_magnetic(hkl, energy_kev=en, azim_zero=aziref, psi=0),
    'xray_resonant': xtl.Scatter.xray_resonant(hkl, energy_kev=en, polarisation='sp', F0=0, F1=1, F2=0, azim_zero=aziref, PSI=[0]).reshape(-1),
    'xray_resonant_magnetic': xtl.Scatter.xray_resonant_magnetic(hkl, energy_kev=en, F0=0, F1=1, F2=0, polarisation='sp', azim_zero=aziref, psi=0),
}

phase = fs.phase_factor(hkl, uvw)
func_inten = {
    'neutron': fs.intensity(fs.structure_factor(scatlength, occupancy, dw, phase)),
    'xray': fs.intensity(fs.structure_factor(ff, occupancy, dw, phase)),
    'xfast': fs.intensity(fs.structure_factor(z, occupancy, dw, phase)),
    'neutron_magnetic': fs.intensity(fs.sf_magnetic_neutron(q, r, occupancy, moment, ffmag, dw)),
    'xray_magnetic': fs.intensity(fs.sf_magnetic_xray(q, r, occupancy, moment, ffmag)),
    'xray_nonresonant_magnetic': fs.intensity((fs.sf_magnetic_xray_beamline(q, r, occupancy, moment, en, ffmag, dw, azi_ref_q=azirefq, psi=0, polarisation='s-p'))),
    'xray_resonant': fs.intensity(fs.sf_magnetic_xray_resonant_alternate(q, r, occupancy, moment, en, debyewaller=dw, polarisation='sp', azi_ref_q=azirefq, psi=0, f0=0, f1=1, f2=0)),
    'xray_resonant_magnetic': fs.intensity(fs.sf_magnetic_xray_resonant(q, r, occupancy, moment, en, debyewaller=dw, azi_ref_q=azirefq, psi=0, polarisation='s-p', f0=0, f1=1, f2=0))
}


def print_inten(key):
    print('\n%s' % key)
    print('  n hkl            class        func        Diff')
    for n in range(len(hkl)):
        print('%3d %2d,%2d,%2d  %10.2f  %10.2f  %10.4f' % (n, *hkl[n], class_inten[key][n], func_inten[key][n], class_inten[key][n]-func_inten[key][n]))


for key in class_inten.keys():
    difrat = 200*np.sum(np.abs(class_inten[key] - func_inten[key]))/np.sum(np.abs(class_inten[key] + func_inten[key]))
    print('%s %6.2f %%'%(key, difrat))
"""
