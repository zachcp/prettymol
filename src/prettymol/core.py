import bpy
import numpy as np
from typing import Union, Any
from biotite.structure.io import pdbx
from biotite import structure as struct
from biotite.structure import bonds
from dataclasses import replace, fields
from molecularnodes.entities.molecule import molecule
from molecularnodes.download import download
from molecularnodes.blender import nodes as bl_nodes

from .repltools import repltools
from .styledata import BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle, BSDFPrincipled, GlareStreaks, GlareBloom, GlareGhosts, GlareFogGlow, GlareSimpleStar



# Connect bonds and center the structure
def load_pdb(code):
    cif_file = download(code)
    structures = pdbx.get_structure(pdbx.CIFFile.read(cif_file))
    arr = next(iter(structures))
    arr.bonds = bonds.connect_via_residue_names(arr)
    arr.coord = arr.coord - np.mean(arr.coord, axis=0)
    return arr


StyleType = Union[BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle]

def draw(arr: Any, style: StyleType, material: BSDFPrincipled) -> None:

    # Create object and material
    molname = f"mol_{id(arr)}"
    matname = f"mol_{id(arr)}_mat"
    obj, _ = molecule._create_object(arr, name=molname, style=style.style)
    bl_nodes.create_starting_node_tree(obj, style=style.style)

    # Setup node tree
    modifier = next(mod for mod in obj.modifiers if mod.type == "NODES")
    node_tree = modifier.node_group
    nodes = node_tree.nodes
    style_node = next((node for node in nodes if "Style" in node.name), None)

    # Create and setup material
    mat = bpy.data.materials.new(matname)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    for input in bsdf.inputs:
        if input.type != "GEOMETRY":
            if value := material.get_by_key(input.name):
                        input.default_value = value

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # Apply style and materials
    if style_node:
        for input in style_node.inputs:
            if input.type != "GEOMETRY":
                if value := style.get_by_key(input.name):
                    input.default_value = value

        # Link material to style node
        material_input = next((inp for inp in style_node.inputs if inp.name == "Material"), None)
        if material_input:
            material_input.default_value = mat

    return None
