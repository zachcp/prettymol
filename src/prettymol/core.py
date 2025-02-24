import bpy
import databpy
import numpy as np
from typing import Union, Any
from biotite.structure.io import pdbx
from biotite.structure import bonds
from molecularnodes.entities.molecule.base import _create_object
from molecularnodes.download import download
from molecularnodes.blender import nodes as bl_nodes
from molecularnodes.blender.nodes import add_custom, get_input, get_output,get_mod, new_tree, styles_mapping

from .materials import Material, MaterialCreator
from .styles import BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle



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
    return arr


StyleType = Union[BallStickStyle, CartoonStyle, RibbonStyle, SpheresStyle, SticksStyle, SurfaceStyle]

# ARR + Styles + Materials (+ Color Map....)
def draw(arr: Any, style: StyleType, material: Material):

    # Create object and material
    molname = f"mol_{id(arr)}"
    matname = f"mol_{id(arr)}_mat"
    obj, _ = _create_object(arr, name=molname)

    # Create and setup material
    mat = bpy.data.materials.new(matname)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    for input in bsdf.inputs:
        if input.type != "GEOMETRY":
            if value := material.get_by_key(input.name):
                        input.default_value = value

    # create the onject with the tyles and material
    create_starting_node_tree_minimal(obj, style=style.style, material=mat)

    # Setup node tree
    modifier = next(mod for mod in obj.modifiers if mod.type == "NODES")
    node_tree = modifier.node_group
    nodes = node_tree.nodes
    style_node = next((node for node in nodes if "Style" in node.name), None)

    # Apply style overrides
    if style_node:
        for input in style_node.inputs:
            if input.type != "GEOMETRY":
                if value := style.get_by_key(input.name):
                    input.default_value = value
    return obj
