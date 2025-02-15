import click
import bpy
from .core import load_pdb, draw
from .materials import Material
from .styles import CartoonStyle
from .repltools import Repltools


@click.command()
@click.option('--code', required=True, help='PDB code of the molecule')
@click.option('--output', required=True, help='Output file path for the rendered image')
def cli(code, output):
    """Generate molecular structure image from code"""

    # load structure
    struct = load_pdb(code)

    # setup the scene
    rt = Repltools()
    rt.set_view_axis(2)

    # draw the molecule
    draw(struct, CartoonStyle(), Material())

    # render the scene
    bpy.context.scene.render.filepath = output
    bpy.ops.render.render(use_viewport=True, write_still=True)
    return "Done"


if __name__ == '__main__':
    cli()
