import bpy
import databpy
import mathutils
import numpy as np
from biotite.structure.io import pdbx
from biotite.structure import filter
from biotite import structure as struct
from biotite.structure import bonds
from molecularnodes.entities.molecule import molecule
from molecularnodes.download import download
from molecularnodes.blender import nodes as bl_nodes
from toolz.dicttoolz import merge
from  .styles import bsdf_principled_defaults, default_styles


# import numpy as np
# from biotite.structure import AtomArray
# from biotite.database import pdbx
# from biotite.structure import bonds
# from biotite.database import download

# Connect bonds and center the structure
def load_pdb(code):
    cif_file = download(code)
    structures = pdbx.get_structure(pdbx.CIFFile.read(cif_file))
    arr = next(iter(structures))
    arr.bonds = bonds.connect_via_residue_names(arr)
    arr.coord = arr.coord - np.mean(arr.coord, axis=0)
    return arr


def create_basic_material(name, stylemap):
     """
     Create a basic material with Principled BSDF node and apply style settings.

     Args:
         name (str): Name of the material
         stylemap (dict): Dictionary of style settings to override defaults

     Returns:
         bpy.types.Material: The created material
     """
     # Create new material and enable nodes
     mat = bpy.data.materials.new(name)
     mat.use_nodes = True
     bsdf = mat.node_tree.nodes.get("Principled BSDF")
     styles = merge(bsdf_principled_defaults, stylemap)

     # Iterate through input sockets
     for input in bsdf.inputs:
         if input.type != "GEOMETRY":
             input_name = input.name
             for key, value in styles.items():
                 if input_name == key:
                     setattr(input, "default_value", value)
     return mat



 # (defn draw! [arr style-key style-map material]
 #   "take a collection of states corresponding to frames and generate an output"
 #   (let [molname (str (gensym))
 #         [obj _] (molecule/_create_object  arr ** :name molname :style (name style-key))
 #         _ (bl_nodes/create_starting_node_tree obj ** :style (name style-key))
 #         modifier (first (filter #(= (.-type %) "NODES") (vec (.-modifiers obj))))
 #         node-tree (.-node_group modifier)
 #         nodes (.-nodes node-tree)
 #         global-styles (merge default-styles style-map)]
 #     (when-let [style-node (first (filter #(str/includes? (.-name %) "Style") (vec nodes)))]
 #       (doseq [input (.-inputs style-node)]
 #         (when (not= (.-type input) "GEOMETRY")
 #           (let [input-name (.-name input)
 #                 styles (get global-styles style-key)]
 #             (doseq [[key value] styles]
 #               (when (= input-name key)
 #                 (println input " " key " " value "")
 #                 (python/setattr input "default_value" value))))))

 #            ;; Set the material in the node's Material input
 #       (when-let [material-input (first (filter #(= (.-name %) "Material") (.. style-node -inputs)))]
 #         (.. obj -data -materials (append material))
 #         (set! (.-default_value material-input) material)))))

def draw(arr, style_key, style_map, material):
    """
    Take a collection of states corresponding to frames and generate an output

    Args:
        arr: Array of molecular states/frames
        style_key: Key indicating the visualization style
        style_map: Dictionary containing style parameters
        material: Material to be applied
    """
    molname = f"mol_{id(arr)}"
    obj, _ = molecule._create_object(arr, name=molname, style=str(style_key))
    bl_nodes.create_starting_node_tree(obj, style=str(style_key))
    modifier = next(mod for mod in obj.modifiers if mod.type == "NODES")
    node_tree = modifier.node_group
    nodes = node_tree.nodes
    global_styles = {**default_styles, **style_map}
    style_node = next((node for node in nodes if "Style" in node.name), None)

    if style_node:
        for input in style_node.inputs:
            if input.type != "GEOMETRY":
                input_name = input.name
                styles = global_styles.get(style_key, {})
                for key, value in styles.items():
                    if input_name == key:
                        print(f"{input} {key} {value}")
                        input.default_value = value

        material_input = next((inp for inp in style_node.inputs if inp.name == "Material"), None)
        if material_input:
            obj.data.materials.append(material)
            material_input.default_value = material
