import bpy
import databpy
import numpy as np
from typing import Union, Any
from biotite.structure import AtomArray, AtomArrayStack
from biotite.structure.io import pdbx
from biotite.structure import bonds
import molecularnodes as mn
from .color import ColorArray
from .materials import Material, MaterialCreator
from .styles import BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle


# Connect bonds and center the structure
def load_pdb(code) -> AtomArray | AtomArrayStack:
    mol = mn.Molecule.load(code)
    arr = mol.array
    return arr


StyleType = Union[BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle]


# ARR + Styles + Materials (+ Color Map....)
def draw(arr: AtomArray, style: StyleType, material: Material):

    arr = ColorArray(arr)
    arr.color_by_element()

    # Create object and material
    molname = f"mol_{id(arr)}"
    matname = f"mol_{id(arr)}_mat"
    mol = Molecule2.from_array(arr, name=molname)
    obj = mol.create_object(style=style.style, color=None, name=f"{molname}")

    # Create and setup material
    mat = bpy.data.materials.new(matname)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    for input in bsdf.inputs:
        if input.type != "GEOMETRY":
            if value := material.get_by_key(input.name):
                        input.default_value = value

    mol.material = mat

    # Setup node tree
    modifier = next(mod for mod in obj.modifiers if mod.type == "NODES")
    # print(modifier)
    node_tree = modifier.node_group
    nodes = node_tree.nodes
    style_node = next((node for node in nodes if "Style" in node.name), None)
    print(style_node)

    # Apply style overrides
    if style_node:
        for input in style_node.inputs:
            if input.type != "GEOMETRY":
                if value := style.get_by_key(input.name):
                    input.default_value = value

    return mol.object
