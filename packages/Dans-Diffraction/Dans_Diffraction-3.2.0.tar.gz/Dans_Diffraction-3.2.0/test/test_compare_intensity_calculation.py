"""
Test calcualtion of structure factors between classes_scattering and functions_scattering

functions_scattering methods:
structure_factor
intensity
phase_factor
phase_factor_qr

sf_magnetic_neutron
sf_magnetic_neutron_polarised
sf_magnetic_xray
sf_neutron
sf_xray
sf_xray_fast
sf_xray_nonresonant_magnetic
sf_xray_resonant

xray_resonant_scattering_factor
scatteringcomponents
scatteringvectors

15/10/2020
"""

import numpy as np
import Dans_Diffraction as dif
from Dans_Diffraction import functions_scattering as fs

# Example crsytals
#xtl = dif.structure_list.Diamond()
#xtl = dif.structure_list.Ca2RuO4()
#xtl = dif.structure_list.Na08CoO2_P63mmc()
# Magnetic structure
xtl = dif.structure_list.Sr3LiRuO6_C2c()

hkl = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1],
       [2, 0, 0], [0, 2, 0], [0, 0, 2], [2, 2, 0], [0, 2, 2], [2, 0, 2], [2, 2, 2],
       [1, 0, 2], [2, 0, 1], [2, 2, 1], [1, 1, 2], [1, 2, 1], [1, 2, 3], [3, 0, 1]]
hkl = np.array(hkl)
# hkl = xtl.Cell.all_hkl(8)

incident_polarisation_vector = ipv = (1, 0, 0)  # relative to unit cell
energy_kev = 2.838  # resonant x-rays only

print(f"\n---Crystal: {xtl.name} ---")
uvw, atom_type, label, occ, uiso, mxmymz = xtl.Structure.get()

xyz = xtl.Cell.calculateR(uvw)
moment = xtl.Cell.moment(mxmymz)
scatteringlength = dif.fc.neutron_scattering_length(atom_type)
element_z = dif.fc.element_z(atom_type)
qval = xtl.Cell.calculateQ(hkl)
qmag = xtl.Cell.Qmag(hkl)
scatteringfactor = dif.fc.xray_scattering_factor(atom_type, qmag)
dbw = dif.fc.debyewaller(uiso, qmag)
magff = dif.fc.magnetic_form_factor(atom_type, qmag)

"""---sf_neutron---"""
inten1 = xtl.Scatter.neutron(hkl)
sf = fs.sf_neutron(hkl, uvw, occ, scatteringlength, dbw)
inten2 = fs.intensity(sf)
print('\nsf_neutron')
print('( h, k, l)  classes_scattering, functions_scattering, difference')
tot_diff = 0
for n in range(len(hkl)):
    h, k, l = hkl[n]
    diff = np.abs(inten2[n]-inten1[n])
    tot_diff += diff
    #print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")

"""---sf_xray---"""
inten1 = xtl.Scatter.x_ray(hkl)
sf = fs.sf_xray(hkl, uvw, occ, scatteringfactor, dbw)
inten2 = fs.intensity(sf)
print('\nsf_xray')
print('( h, k, l)  classes_scattering, functions_scattering, difference')
tot_diff = 0
for n in range(len(hkl)):
    h, k, l = hkl[n]
    diff = np.abs(inten2[n]-inten1[n])
    tot_diff += diff
    #print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")

"""---sf_xray_fast---"""
inten1 = xtl.Scatter.x_ray_fast(hkl)
sf = fs.sf_xray_fast(hkl, uvw, occ, element_z, dbw)
inten2 = fs.intensity(sf)
print('\nsf_xray_fast')
print('( h, k, l)  classes_scattering, functions_scattering, difference')
tot_diff = 0
for n in range(len(hkl)):
    h, k, l = hkl[n]
    diff = np.abs(inten2[n]-inten1[n])
    tot_diff += diff
    #print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")


if xtl.Structure.ismagnetic():
    print('\n------Magnetic Calculations------\n')

    """---sf_magnetic_neutron---"""
    xtl.Scatter._polarised = False
    inten1 = xtl.Scatter.magnetic_neutron(hkl)
    sf = fs.sf_magnetic_neutron(qval, xyz, occ, moment, magnetic_formfactor=magff, debyewaller=dbw)
    inten2 = fs.intensity(sf)
    print('\nsf_magnetic_neutron')
    print('( h, k, l)  classes_scattering, functions_scattering, difference')
    tot_diff = 0
    for n in range(len(hkl)):
        h, k, l = hkl[n]
        diff = np.abs(inten2[n]-inten1[n])
        tot_diff += diff
        print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
    print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")

    """---sf_magnetic_neutron_polarised---"""
    xtl.Scatter._polarised = True
    xtl.Scatter._polarisation_vector_incident = ipv
    inten1 = xtl.Scatter.magnetic_neutron(hkl)
    sf = fs.sf_magnetic_neutron_polarised(qval, xyz, occ, moment, incident_polarisation_vector=ipv,
                                          magnetic_formfactor=magff, debyewaller=dbw)
    inten2 = fs.intensity(sf)
    print('\nsf_magnetic_neutron_polarised %s' % list(ipv))
    print('( h, k, l)  classes_scattering, functions_scattering, difference')
    tot_diff = 0
    for n in range(len(hkl)):
        h, k, l = hkl[n]
        diff = np.abs(inten2[n] - inten1[n])
        tot_diff += diff
        print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
    print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")

    """---sf_magnetic_xray---"""
    xtl.Scatter._polarised = False
    inten1 = xtl.Scatter.xray_magnetic(hkl)
    sf = fs.sf_magnetic_xray(qval, xyz, occ, moment, magnetic_formfactor=magff, debyewaller=dbw)
    inten2 = fs.intensity(sf)
    print('\nsf_magnetic_xray')
    print('( h, k, l)  classes_scattering, functions_scattering, difference')
    tot_diff = 0
    for n in range(len(hkl)):
        h, k, l = hkl[n]
        diff = np.abs(inten2[n] - inten1[n])
        tot_diff += diff
        print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
    print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")

    """---sf_magnetic_xray_polarised---"""
    xtl.Scatter._polarised = True
    xtl.Scatter._polarisation_vector_incident = ipv
    inten1 = xtl.Scatter.xray_magnetic(hkl)
    sf = fs.sf_magnetic_xray_polarised(qval, xyz, occ, moment, incident_polarisation_vector=ipv,
                                       magnetic_formfactor=magff, debyewaller=dbw)
    inten2 = fs.intensity(sf)
    print('\nsf_magnetic_xray_polarised %s' % list(ipv))
    print('( h, k, l)  classes_scattering, functions_scattering, difference')
    tot_diff = 0
    for n in range(len(hkl)):
        h, k, l = hkl[n]
        diff = np.abs(inten2[n] - inten1[n])
        tot_diff += diff
        print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
    print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")

    """---sf_xray_nonresonant_magnetic---"""
    inten1 = xtl.Scatter.xray_nonresonant_magnetic(hkl, energy_kev, azim_zero=[1, 0, 0], psi=0, polarisation='s-p')
    sf = fs.sf_xray_nonresonant_magnetic(qval, xyz, occ, moment, energy_kev, azi_ref_q=(1, 0, 0), psi=0,
                                         polarisation='s-p')
    inten2 = fs.intensity(sf)
    print('\nsf_xray_nonresonant_magnetic sp psi=0 (100)')
    print('( h, k, l)  classes_scattering, functions_scattering, difference')
    tot_diff = 0
    for n in range(len(hkl)):
        h, k, l = hkl[n]
        diff = np.abs(inten2[n] - inten1[n])
        tot_diff += diff
        print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
    print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")

    """---sf_xray_resonant---"""
    inten1 = xtl.Scatter.xray_resonant(hkl, energy_kev, polarisation='sp', F0=1, F1=1, F2=1,
                                       azim_zero=(1, 0, 0), PSI=0)
    sf = fs.sf_xray_resonant(qval, xyz, occ, moment, energy_kev, polarisation='sp', f0=1, f1=1, f2=1,
                             azi_ref_q=(1, 0, 0), psi=0, debyewaller=dbw)
    inten2 = fs.intensity(sf)
    print('\nsf_xray_resonant sp psi=0 (100)')
    print('( h, k, l)  classes_scattering, functions_scattering, difference')
    tot_diff = 0
    for n in range(len(hkl)):
        h, k, l = hkl[n]
        diff = np.abs(inten2[n] - inten1[n, 0])
        tot_diff += diff
        print(f"{h:2.0f},{k:2.0f},{l:2.0f}  {inten1[n, 0]:10.2f}  {inten2[n]:10.2f}  {diff:6.4f}")
    print(f"Total difference after {n+1} reflections: {tot_diff:6.4f}, with max intensity: {inten2.max(): 6.4g}")


