import copy
import bpy
import databpy
import numpy as np
from typing import Union, Any
from biotite.structure import AtomArray, AtomArrayStack
import molecularnodes as mn
from .color import ColorArray
from .materials import Material, MaterialCreator
from .styles import BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle


class Mol2(mn.Molecule):
    def __init__(self, array, reader=None):
        super().__init__(array, reader=None)

    @classmethod
    def load_code(cls, code):
        mol = mn.Molecule.fetch(code)
        arr = copy.copy(mol.array)
        # deletes the object with the code name after copying the aray
        bpy.data.objects.remove(mol.object)
        return arr[0]

    def apply_style(self):
        print(self.tree)





StyleType = Union[BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle]


# ARR + Styles + Materials (+ Color Map....)
def draw(arr: AtomArray, style: StyleType | str, material: Material | str ):
    # arr = ColorArray(arr)
    # arr.color_by_element()
    # Create object and material

    if isinstance(style, str):
        style_name = style
    else:
        style_name = style.style

    if isinstance(material, str):
        material_name = material
    else:
        material_name = material.materialize()
    mol = mn.Molecule(array=arr, reader=None).add_style(style=style_name, material=material_name)
    return mol.object
