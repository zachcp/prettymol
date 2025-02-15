import click
import bpy
from .core import load_pdb, draw
from .materials import Material
from .styles import CartoonStyle, SpheresStyle
from .repltools import Repltools
from .selections import StructureSelector


@click.command()
@click.option('--code', required=True, help='PDB code of the molecule')
@click.option('--output', required=True, help='Output file path for the rendered image')
def cli(code, output):
    """Generate molecular structure image from code"""

    rt = Repltools()
    rt.set_view_axis(distance=2)

    # load structure
    structure = load_pdb(code)

    # setup the scene
    polymer = StructureSelector(structure).amino_acids().get_selection()
    ligand = StructureSelector(structure).resname("MYN").get_selection()

    # draw the molecu
    draw(polymer, CartoonStyle(), Material())
    draw(ligand, SpheresStyle(), Material())

    # render the scene
    bpy.context.scene.render.filepath = output
    bpy.ops.render.render(use_viewport=True, write_still=True)
    return "Done"


if __name__ == '__main__':
    cli()
