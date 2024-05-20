"""
Dans_Diffraction
Start GUI script
"""

import Dans_Diffraction as dif
from Dans_Diffraction.tkgui.scattering import ReflectionSelectionBox, tk

xtl = dif.structure_list.Ca2RuO4()
parent = tk.Tk()
output = ReflectionSelectionBox(xtl, parent=parent).show()

print(output)
parent.destroy()

print('Finished!')
