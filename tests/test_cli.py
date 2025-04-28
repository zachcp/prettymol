import os
from prettymol.cli import cli, render
from click.testing import CliRunner



def test_render_internasl():
    import molecularnodes as mn
    mn.register()
    import os
    import math
    from math import radians

    import bpy
    import click
    from PIL import Image
    from pathlib import Path

    from prettymol.core import draw, Mol2
    from prettymol.lighting import LightingCreator
    from prettymol.materials import MaterialCreator
    from prettymol.repltools import Repltools
    from prettymol.selections import StructureSelector
    from prettymol.styles import StyleCreator
    import molecularnodes as mn

    code = "1FAP"
    outut = "test.gif"

    rt = Repltools()
    rt.view_set_axis(distance=2)

    # load structure
    structure =  Mol2.load_code(code)
    print("Structure loaded")

    # setup the scene
    polymer = StructureSelector(structure).amino_acids().get_selection()
    ligand = StructureSelector(structure).ligand().get_selection()
    print("Polymer and ligand loaded")


    # draw the molecule
    draw(polymer, StyleCreator.cartoon(), MaterialCreator.new())
    draw(ligand, StyleCreator.spheres(),  MaterialCreator.new())


def test_render_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(render, ['--code', '1fap', '--output', 'test.png'])
        assert result.exit_code == 0
        assert os.path.exists('test.png')
