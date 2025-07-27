import copy
import bpy
import numpy as np
from typing import Union, Any
from biotite.structure import AtomArray
import molecularnodes as mn
from .color import ColorArray
from .materials import Material, MaterialCreator
from .styles import BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle
import numpy as np
from .selection_functions import *
from molecularnodes.nodes.nodes import create_starting_node_tree


StyleType = Union[BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle]


class Prettymol():
    def __init__(self, array: AtomArray):
        self.array = array
        self.transforamttons = None
        self.selections = []

    @classmethod
    def load_code(cls, code):
        mol = mn.Molecule.fetch(code)
        arr = copy.copy(mol.array)[0]
        # deletes the object with the code name after copying the aray
        bpy.data.objects.remove(mol.object)
        arr.coord = arr.coord - np.mean(arr.coord, axis=0)
        return Prettymol(arr)



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

        # process  selections first
        if selection is None:
            mask = np.ones(len(self.array), dtype=bool)
        elif isinstance(selection, list):
            if not selection:  # Empty list
                mask = np.ones(len(self.array), dtype=bool)
            else:
                mask = np.ones(len(self.array), dtype=bool)
                for sel_func in selection:
                    if callable(sel_func):
                        result = sel_func(self.array)
                        mask = mask & result
                    else:
                        raise TypeError(f"Selection must be callable, got {type(sel_func)}")
        elif callable(selection):
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


    def _process_selections(self):
        pass


    # Note: In mn.nodes.geometry:
    #   assign_material
    #   add_style_branch
    def draw(self):
        # apply transformations

        # iterate through each set of selections
        #    - create a new AtomArray if there is a selection
        #    - apply the color_fn if there is one
        #    - create the MN Molecule and Blender Object
        #    - apply the style and the material
        for idx, selection in enumerate(self.selections):
            print(f"idx, {idx}, selection: {selection}")
            mask = selection['mask']
            color = selection['color']
            style = selection['style']
            material = selection['material']
            new_arr = copy.deepcopy(self.array[mask])
            print(style, material)
            # need to apply the color fns here.
            new_arr.set_annotation("Color", np.array([ [1., 0.2, 0.2] for _ in range(len(new_arr))]))
            mol = mn.Molecule(array=new_arr, reader=None)
            mol.create_object()
            mol.add_style(style, color=None, material = material)

        return self






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
        material_name = material.blenderize()

    mol = mn.Molecule(array=arr, reader=None)
    mol.create_object()
    print(mol)
    print(mol.object.uuid)
    #.add_style(style=style_name, material=material_name)
    return mol.object
