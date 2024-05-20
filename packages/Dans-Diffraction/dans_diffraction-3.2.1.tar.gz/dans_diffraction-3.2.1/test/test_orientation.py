"""
Test orientation matrix calculations

26/9/2021
"""

import numpy as np
import matplotlib.pyplot as plt

import Dans_Diffraction as dif

dif.fg.nice_print()

xtl = dif.structure_list.Na08CoO2_P63mmc()

uv = xtl.Cell.UV()
u = dif.fc.umatrix(a_axis=[1, 0, 0], c_axis=[0, 0, 1])
lab = np.eye(3)  # None

dif.fp.plot_diffractometer_reciprocal_space(phi=30, chi=90, eta=10, mu=0, delta=20, gamma=0, uv=uv, u=u, lab=lab, energy_kev=8)
