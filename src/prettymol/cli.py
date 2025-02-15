import click
import bpy
from .core import load_pdb, draw
from .materials import Material
from .styles import CartoonStyle


@click.command()
@click.argument('code')
@click.argument('output')
def cli(code, output):
    """Generate molecular structure image from code"""
    struct = load_pdb(code)

    draw(struct, CartoonStyle(), Material())

    bpy.context.scene.render.filepath = output
    bpy.ops.render.render(use_viewport=True, write_still=True)
    return "Done"


if __name__ == '__main__':
    cli()
