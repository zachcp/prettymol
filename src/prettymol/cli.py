import bpy
import click
from .core import load_pdb, draw
from .lighting import LightingCreator
from .materials import MaterialCreator
from .repltools import Repltools
from .selections import StructureSelector
from .styles import StyleCreator



@click.group()
def cli():
    """Molecular structure visualization tool"""
    pass


@click.command()
@click.option('--code', required=True, help='PDB code of the molecule')
@click.option('--output', required=True, help='Output file path for the rendered image')
def render(code, output):
    """Generate molecular structure image from code"""

    rt = Repltools()
    rt.view_set_axis(distance=2)

    # load structure
    structure = load_pdb(code)

    # setup the scene
    polymer = StructureSelector(structure).amino_acids().get_selection()
    ligand = StructureSelector(structure).resname("RAP").get_selection()

    # draw the molecu
    draw(polymer, StyleCreator.cartoon(), MaterialCreator.new())
    draw(ligand, StyleCreator.spheres(),  MaterialCreator.new())

    # render the scene
    bpy.context.scene.render.filepath = output
    bpy.ops.render.render(use_viewport=True, write_still=True)
    return "Done"


@cli.command()
@click.option('--code', required=True, help='PDB code of the molecule')
@click.option('--output', required=True, help='Output directory path')
@click.option('--selection', default=None, help='Optional selection criteria')
def grow(code, output, selection):
    """Generate growth animation from molecular structure"""
    # Add your implementation here
    click.echo(f"Growing structure {code} with output to {output}")
    if selection:
        click.echo(f"Using selection: {selection}")
    return "Done"



if __name__ == '__main__':
    cli()
