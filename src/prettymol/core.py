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

from .selection_functions import *

StyleType = Union[BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle]


class Prettymol():
    def init__(self, array: AtomArray):
        self.array = array
        self.transforamttons = None
        self.selections = []

  def add_selection(self, selection=None, color=None, style=None, material=None):
        """
        Add selection(s) to the molecule.

        Parameters:
        - selection: A single selection function or a list of selection functions to be combined.
                     Each function should be a curried function that takes a structure and returns a mask.
        - color: Color to apply to the selection
        - style: Style to apply
        - material: Material to apply

        Returns:
        - self (for method chaining)
        """

        # process  selecitons fist
        if selection is None:
            # No selection means select all atoms
            mask = np.ones(len(self.array), dtype=bool)
        elif isinstance(selection, list):
            # Process a list of selection functions
            if not selection:  # Empty list
                mask = np.ones(len(self.array), dtype=bool)
            else:
                # Start with all atoms selected
                mask = np.ones(len(self.array), dtype=bool)
                # Apply each selection function and combine with AND
                for sel_func in selection:
                    if callable(sel_func):
                        result = sel_func(self.array)
                        mask = mask & result
                    else:
                        raise TypeError(f"Selection must be callable, got {type(sel_func)}")
        elif callable(selection):
            # Single selection function
            mask = selection(self.array)
        else:
            raise TypeError("Selection must be a callable, a list of callables, or None")

        # then add color fns


        # then add style



        # then add materials


        self.selections.append({
            'mask': mask,
            'color': color,
            'style': style,
            'material': material
        })

        return self

    def draw(self):
        # apply transformations

        # iterate through each set of selections
        #    - create a new AtomArray if there is a selection
        #    - apply the color_fn if there is one
        #    - create the MN Molecule and Blender Object
        #    - apply the style and the material

        pass


class Mol2():
    def __init__(self,
        array,
        style:  StyleType | str = None,
        material:  Material | str = None):

        # handle styles
        if style is None:
           self.style = "cartoon"
        elif isinstance(style, str):
            self.style = style
        else:
            self.style = style.style

        # handle materials
        #         # handle styles
        if material is None:
           self.material = "cartoon"
        elif isinstance(material, str):
            self.material = material
        else:
            self.material = material.materialize()


    @classmethod
    def load_code(cls, code):
        mol = mn.Molecule.fetch(code)
        arr = copy.copy(mol.array)
        # deletes the object with the code name after copying the aray
        bpy.data.objects.remove(mol.object)
        return arr[0]

    def apply_style(self):
        print(self.tree)

    def draw(self):
        mol = mn.Molecule(array=self.array, reader=None)
        mol.create_object()
        print(mol)
        print(mol.object.uuid)
        #.add_style(style=style_name, material=material_name)
        return mol.object





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

    mol = mn.Molecule(array=arr, reader=None)
    mol.create_object()
    print(mol)
    print(mol.object.uuid)
    #.add_style(style=style_name, material=material_name)
    return mol.object
