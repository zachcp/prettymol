import bpy
import databpy
import numpy as np
from typing import Union, Any
from biotite.structure import AtomArray, AtomArrayStack
from biotite.structure.io import pdbx
from biotite.structure import bonds
from molecularnodes.entities.molecule.base import _create_object, Molecule
from molecularnodes.download import download
from molecularnodes.blender import nodes as bl_nodes
from molecularnodes.blender.nodes import add_custom, get_input, get_output,get_mod, new_tree, styles_mapping

from .color import ColorArray
from .materials import Material, MaterialCreator
from .styles import BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle

from .molecule import Molecule2

# Modified form the original:
# https://github.com/BradyAJohnston/MolecularNodes/blob/main/molecularnodes/blender/nodes.py
# removes the color nodes to make a dead-simple node.
def create_starting_node_tree_minimal(
    object: bpy.types.Object,
    coll_frames: bpy.types.Collection | None = None,
    style: str = "spheres",
    name: str | None = None,
    color: str = "common",
    material: str = "MN Default",
    is_modifier: bool = True,
) -> None:
    mod = get_mod(object)
    if not name:
        name = f"MN_{object.name}"

    try:
        tree = bpy.data.node_groups[name]
        mod.node_group = tree
        return
    except KeyError:
        pass

    tree = new_tree(name, input_name="Atoms")
    tree.is_modifier = is_modifier
    link = tree.links.new
    mod.node_group = tree

    # move the input and output nodes for the group
    node_input = get_input(tree)
    node_output = get_output(tree)
    node_input.location = [0, 0]
    node_output.location = [700, 0]
    node_style = add_custom(tree, styles_mapping[style], [450, 0], material=material)
    link(node_style.outputs[0], node_output.inputs[0])
    link(node_input.outputs[0], node_style.inputs[0])
    return None

# Connect bonds and center the structure
def load_pdb(code):
    cif_file = download(code)
    structures = pdbx.get_structure(pdbx.CIFFile.read(cif_file))
    arr = next(iter(structures))
    arr.bonds = bonds.connect_via_residue_names(arr)
    arr.coord = arr.coord - np.mean(arr.coord, axis=0)
    #arr = ColorArray(arr) # this will provide methods related to color
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
