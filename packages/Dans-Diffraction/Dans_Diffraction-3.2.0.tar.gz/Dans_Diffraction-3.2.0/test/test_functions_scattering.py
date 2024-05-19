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
opt = fs.options(occ=occupancy, debyewaller=None, moment=moment, magnetic_formfactor=ffmag, energy_kev=en,
                 polarisation='sp', azi_ref_q=azirefq, psi=0, f0=0, f1=1, f2=0)
optdw = fs.options(occ=occupancy, debyewaller=dw, moment=moment, magnetic_formfactor=ffmag, energy_kev=en,
                   polarisation='sp', azi_ref_q=azirefq, psi=0, f0=0, f1=1, f2=0)

xtl.Scatter._use_isotropic_thermal_factor = True
xtl.Scatter._use_magnetic_form_factor = True

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
    'neutron_magnetic': fs.intensity(fs.sf_magnetic_neutron(q, r, **opt)),  # Scatter.magnetic_neutron doesnt use dw
    'xray_magnetic': fs.intensity(fs.sf_magnetic_xray(q, r, **opt)),  # Scatter.xray_magnetic doesnt use dw
    'xray_nonresonant_magnetic': fs.intensity((fs.sf_magnetic_xray_beamline(q, r, **optdw))),
    'xray_resonant': fs.intensity(fs.sf_magnetic_xray_resonant_alternate(q, r, **optdw)),
    'xray_resonant_magnetic': fs.intensity(fs.sf_magnetic_xray_resonant(q, r, **optdw))
}


def print_inten(key):
    print('\n%s' % key)
    print('  n hkl            class        func        Diff')
    for n in range(len(hkl)):
        print('%3d %2d,%2d,%2d  %10.2f  %10.2f  %10.4f' % (n, *hkl[n], class_inten[key][n], func_inten[key][n], class_inten[key][n]-func_inten[key][n]))


for key in class_inten.keys():
    difrat = 200*np.sum(np.abs(class_inten[key] - func_inten[key]))/np.sum(np.abs(class_inten[key] + func_inten[key]))
    print('%s %6.2f %%'%(key, difrat))


# Find difference in xray_resonant_magnetic
print_inten('xray_resonant_magnetic')

# xray_resonant_magnetic uses scatteringvectors function
# no significant differences found
kin1, kout1, ein1, eout1 = xtl.Scatter.scatteringvectors(hkl, en, aziref, 0, 's-p')
kin2, kout2, ein2, eout2 = fs.scatteringvectors(q, en, azirefq, 0, 's-p')
print('\n\nCompare scatteringvectors')
for n in range(len(hkl)):
    print(hkl[n], '%10.5g %10.5g %10.5g %10.5g' % (dif.fg.mag(kin2[n]-kin1[n]), dif.fg.mag(kout2[n]-kout1[n]), dif.fg.mag(ein2[n]-ein1[n]), dif.fg.mag(eout2[n]-eout1[n])))
"""
# Compare (2,0,1) azimuth
psivals = np.arange(-180, 101, 2)
q003 = xtl.Cell.calculateQ([2,0,1])
fxres1 = [xtl.Scatter.xray_resonant_scattering_factor([2,0,1], en, polarisation='sp', F0=0,F1=1,F2=0,azim_zero=aziref,psi=psi) for psi in psivals]
fxres2 = [fs.xray_resonant_scattering_factor(q003, mxmymz, en, polarisation='sp', flm=(0, 1, 0), psi=psi, azi_ref_q=azirefq) for psi in psivals]

plt.figure(figsize=[12, 10], dpi=60)
plt.plot(psivals, fxres1, '-', lw=3, label='Scatter.xray_resonant_scattering_factor')
plt.plot(psivals, fxres2, '-', lw=3, label='fs.xray_resonant_scattering_factor')
plt.xlabel('psi')
plt.title('E = %1.4f keV hkl = (2,0,1)' % en, fontsize=20)
plt.legend(loc=0, frameon=False)
plt.show()
"""

# Compare resonant x-ray functions
print('\n\n resonant x-ray functions')
print('  n hkl       xray_resonant  xray_resonant_magnetic  Diff')
for n in range(len(hkl)):
    print('%3d %2d,%2d,%2d  %10.2f  %10.2f  %10.4f' % (n, *hkl[n], func_inten['xray_resonant'][n],
                                                       func_inten['xray_resonant_magnetic'][n],
                                                       func_inten['xray_resonant'][n]/func_inten['xray_resonant_magnetic'][n]))



# Test Speed of functions
psivals = np.arange(-180, 181)
import time
t0 = time.process_time()
xr1 = fs.intensity(fs.sf_magnetic_xray_resonant(q, r, **opt)),
t1 = time.process_time()
xr2 = fs.intensity(fs.sf_magnetic_xray_resonant_alternate(q, r, **opt))
t2 = time.process_time()

print('          sf_magnetic_xray_resonant: %s s' % (t1-t0))
print('sf_magnetic_xray_resonant_alternate: %s s' % (t2-t1))
print('Difference over %4d refs x %3d psi = %6d values: %s' % (len(q), len(psivals), xr2.size, np.sum(xr2-xr1)))
