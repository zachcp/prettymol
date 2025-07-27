import pytest
import bpy
from prettymol.materials import Material, MaterialCreator

@pytest.fixture
def cleanup_materials():
    """Clean up any materials created during tests"""
    # Store existing materials before test
    existing_materials = set(bpy.data.materials.keys())

    yield

    # Remove materials created during test
    for material in list(bpy.data.materials):
        if material.name not in existing_materials:
            bpy.data.materials.remove(material)


def test_materialize_returns_blender_material(cleanup_materials):
    """Test that materialize() returns a Blender material"""
    # Create a material
    material = Material()
    blender_material = material.blenderize()

    # Check that it's a Blender material
    assert isinstance(blender_material, bpy.types.Material)


def test_materialize_with_custom_name(cleanup_materials):
    """Test that materialize() uses the provided name"""
    # Create a material with a specific name
    material = Material()
    name = "test_custom_material"
    blender_material = material.blenderize(name)

    # Check that the name matches
    assert blender_material.name == name
    # Check that it's in Blender's materials collection
    assert name in bpy.data.materials
    assert bpy.data.materials[name] == blender_material


def test_materialize_with_auto_name(cleanup_materials):
    """Test that materialize() generates a name if none is provided"""
    # Create a material without specifying a name
    material = Material()
    blender_material = material.blenderize()

    # Check that the name starts with "material_"
    assert blender_material.name.startswith("material_")
    # Check that it's in Blender's materials collection
    assert blender_material.name in bpy.data.materials
    assert bpy.data.materials[blender_material.name] == blender_material


def test_material_creator_preset(cleanup_materials):
    """Test that a material from MaterialCreator can be materialized"""
    # Create a preset material
    material = MaterialCreator.glass()
    name = "test_glass_material"
    blender_material = material.blenderize(name)

    # Check that it's a Blender material with the correct name
    assert isinstance(blender_material, bpy.types.Material)
    assert blender_material.name == name
    assert name in bpy.data.materials
