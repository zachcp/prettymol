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
@click.option('--width', default=800, help='Width of output images')
@click.option('--height', default=800, help='Height of output images')
@click.option('--rotation-steps', default=360, help='Number of rotation steps')
@click.option('--selection', default=None, help='Optional selection criteria')
def grow(code, output, width, height, rotation_steps, selection):
    """Generate growth animation from molecular structure"""

    # Create output directory if it doesn't exist
    os.makedirs(output, exist_ok=True)

    rt = Repltools()
    rt.view_set_axis(distance=1.0)

    # Load and orient structure
    structure = load_pdb(code)
    structure = orient_principal_components(structure, order=(1, 2, 0))

    # Get residue IDs for progressive building
    polymer = StructureSelector(structure).amino_acids().get_selection()
    resids = list(set(polymer.get_annotation('res_id').tolist()))

    # Phase 1: Grow the backbone
    for i in range(len(resids)):
        if i % 2 == 0:  # Only process every other frame to reduce total frames
            rt.scene_clear()

            # Select progressively more residues
            sel = StructureSelector(structure)
            sel2 = sel.resids(resids[:i]).get_selection()

            # Draw the current selection
            obj_structure = draw(
                sel2,
                StyleCreator.ribbon().update_properties(radius=1, quality=2, shade_smooth=False),
                MaterialCreator.new()
            )

            # Rotate the structure
            mesh1 = bsyn.Mesh(obj_structure, class_id=0)
            mesh1.rotate_by([0, 0, radians(i)])

            # Save the frame
            rt.view_set_axis(distance=1)
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
                chromo = StructureSelector(structure).resname("CRO").get_selection()
                intensity = 5 + round(3 * math.sin(i), 2)
                obj_chromo = draw(
                    chromo,
                    StyleCreator.spheres(),
                    MaterialCreator.green_glow().update_properties(emission_strength=intensity)
                )
            except:
                click.echo("No chromophore (CRO) found in structure")

            # Rotate all components
            for obj in [obj_structure, obj_surface]:
                mesh = bsyn.Mesh(obj, class_id=0)
                mesh.rotate_by([0, 0, radians(frame)])

            # Save the frame
            rt.view_save(
                filename=f"{output}/frame_{frame:03d}",
                width=width,
                height=height
            )

    click.echo(f"Animation frames saved to {output}")
    return "Done"


if __name__ == '__main__':
    cli()
