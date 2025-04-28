import os
import math
from math import radians

import bpy
import click
from PIL import Image
from pathlib import Path

from .core import draw, Mol2
from .lighting import LightingCreator
from .materials import MaterialCreator
from .repltools import Repltools
from .selections import StructureSelector
from .styles import StyleCreator
import molecularnodes as mn


@click.group()
def cli():
    """Molecular structure visualization tool"""
    pass


@cli.command()
@click.option('--code', required=True, help='PDB code of the molecule')
@click.option('--output', required=True, help='Output file path for the rendered image')
def render(code, output):
    """Generate molecular structure image from code"""

    mn.register()


    rt = Repltools()
    rt.view_set_axis(distance=2)

    # load structure
    structure =  Mol2.load_code(code)
    print(structure)

    # setup the scene
    polymer = StructureSelector(structure).amino_acids().get_selection()
    ligand = StructureSelector(structure).ligand().get_selection()
    print(polymer)
    print(ligand)

    # draw the molecule
    draw(polymer, StyleCreator.cartoon(), MaterialCreator.new())
    draw(ligand, StyleCreator.spheres(),  MaterialCreator.new())

    print("Pre-render")
    # render the scene
    bpy.context.scene.render.filepath = output
    bpy.ops.render.render(use_viewport=True, write_still=True)
    return "Done"



@cli.command()
@click.option('--code', required=True, help='PDB code of the molecule')
@click.option('--output', required=True, help='Output directory path')
@click.option('--width', default=400, help='Width of output images')
@click.option('--height', default=400, help='Height of output images')
@click.option('--camera-distance', default=2.0, help='Camaeras Distance from the origin')
@click.option('--rotation-steps', default=360, help='Number of rotation steps')
@click.option('--selection', default=None, help='Optional selection criteria')
def grow(code, output, width, height, camera_distance, rotation_steps, selection):
    """Generate growth animation from molecular structure"""

    # Create output directory if it doesn't exist
    os.makedirs(output, exist_ok=True)
    # Set up transparent background
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.film_transparent = True

    rt = Repltools()
    rt.view_set_axis(distance=camera_distance)

    # Load and orient structure
    structure = Mol2.load_code(code)
    polymer = StructureSelector(structure).amino_acids().get_selection()
    resids = list(set(polymer.get_annotation('res_id').tolist()))

    # Phase 1: Grow the backbone
    for i in range(len(resids)):
        if i % 2 == 0:
            rt.scene_clear()
            sel = StructureSelector(structure)
            sel2 = sel.resids(resids[:i]).get_selection()
            obj_structure = draw(
                sel2,
                StyleCreator.ribbon().update_properties(radius=1, quality=2, shade_smooth=False),
                MaterialCreator.new()
            )

            # Rotate using Blender's rotation
            obj_structure.rotation_euler.z = radians(i)

            # Save the frame
            rt.view_set_axis(distance=camera_distance)
            rt.view_save(
                filename=f"{output}/frame_{i:03d}",
                width=width,
                height=height
            )

    # Phase 2: Add surface and chromophore with rotation
    base_rotation = len(resids)  # Continue from where backbone growth ended

    for i in range(rotation_steps):
        if i % 2 == 0:
            frame = base_rotation + i
            rt.scene_clear()

            # Draw complete backbone
            obj_structure = draw(
                polymer,
                StyleCreator.ribbon().update_properties(radius=1, quality=2, shade_smooth=False),
                MaterialCreator.new()
            )

            # Add surface
            obj_surface = draw(
                polymer,
                StyleCreator.surface(),
                MaterialCreator.glass().update_properties(alpha=0.2)
            )

            # Add chromophore if present
            try:

                ligand = StructureSelector(structure).ligand().get_selection()
                intensity = 5 + round(3 * math.sin(i), 2)
                obj_chromo = draw(
                    ligand,
                    StyleCreator.spheres(),
                    MaterialCreator.green_glow().update_properties(emission_strength=intensity)
                )
                # Rotate chromophore
                obj_chromo.rotation_euler.z = radians(frame)
            except:
                click.echo("No ligand found in structure")

            # Rotate all components
            obj_structure.rotation_euler.z = radians(frame)
            obj_surface.rotation_euler.z = radians(frame)

            # Save the frame
            rt.view_save(
                filename=f"{output}/frame_{frame:03d}",
                width=width,
                height=height
            )

    click.echo(f"Animation frames saved to {output}")

    click.echo(f"Creating GIF from PNGs.....")

    # Get list of PNG files
    frames = []
    png_files = Path(f"{output}").glob("*.png")
    png_files = sorted(list(png_files))

    # Open each PNG and append to frames
    for filename in png_files:
        frame = Image.open(filename)
        frames.append(frame)

    frames[0].save(
        f'{output}.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=50,  # Duration for each frame in milliseconds
        disposal=2,
        loop=0  # 0 means loop forever
    )

    click.echo(f"GIF Creation Complete!")
    return "Done"


if __name__ == '__main__':
    cli()
