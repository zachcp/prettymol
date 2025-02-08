"""Constant style definitions for molecular visualization in Blender.

This module contains predefined style settings for different molecular visualization
modes including ball-and-stick, cartoon, ribbon, spheres, sticks and surface
representations. It also includes default materials settings for the Principled
BSDF shader.
"""

default_styles = {
    'ball+stick': {
        "Quality": 2,
        "As Mesh": True,
        "Sphere Radii": 0.3,
        "Bond Split": False,
        "Bond Find": False,
        "Bond Radius": 0.3,
        "Color Blur": False,
        "Shade Smooth": True
    },
    'cartoon': {
        "Quality": 2,
        "DSSP": False,
        "Cylinders": False,
        "Arrows": True,
        "Rounded": False,
        "Thickness": 0.6,
        "Width": 2.2,
        "Loop Radius": 0.3,
        "Smoothing": 0.5,
        "Color Blur": False,
        "Shade Smooth": True
    },
    'ribbon': {
        "Quality": 3,
        "Radius": 1.6,
        "Smoothing": 0.6,
        "Color Blur": False,
        "Shade Smooth": False
    },
    'spheres': {
        "As Mesh": True,
        "Radii": 0.8,
        "Subdivisions": 2,
        "Shade Smooth": False
    },
    'sticks': {
        "Quality": 2,
        "Radius": 0.2,
        "Color Blur": False,
        "Shade Smooth": False
    },
    'surface': {
        "Quality": 3,
        "Separate": True,
        "Attribute": "chain_id",
        "Scale Radii": 1.5,
        "Probe Size": 1.0,
        "Triangulate": False,
        "Relaxation Steps": 10,
        "by CA": False,
        "Blur": 2,
        "Shade Smooth": True
    }
}

bsdf_principled_defaults = {
    "Base Color": [0.8, 0.8, 0.8, 1.0],
    "Metallic": 0.0,
    "Roughness": 0.2085610330104828,
    "IOR": 1.4500000476837158,
    "Alpha": 1.0,
    "Normal": [0.0, 0.0, 0.0],
    "Weight": 0.0,
    "Diffuse Roughness": 0.0,
    "Subsurface Weight": 0.0,
    "Subsurface Radius": [1.0, 0.2, 0.1],
    "Subsurface Scale": 0.05000000074505806,
    "Subsurface IOR": 1.399999976158142,
    "Subsurface Anisotropy": 0.0,
    "Specular IOR Level": 0.5,
    "Specular Tint": [1.0, 1.0, 1.0, 1.0],
    "Anisotropic": 0.0,
    "Anisotropic Rotation": 0.0,
    "Tangent": [0.0, 0.0, 0.0],
    "Transmission Weight": 0.0,
    "Coat Weight": 0.0,
    "Coat Roughness": 0.029999999329447746,
    "Coat IOR": 1.5,
    "Coat Tint": [1.0, 1.0, 1.0, 1.0],
    "Coat Normal": [0.0, 0.0, 0.0],
    "Sheen Weight": 0.0,
    "Sheen Roughness": 0.5,
    "Sheen Tint": [0.5, 0.5, 0.5, 1.0],
    "Emission Color": [0.0, 0.0, 0.0, 1.0],
    "Emission Strength": 0.0,
    "Thin Film Thickness": 0.0,
    "Thin Film IOR": 1.3300000429153442
}



glare_defaults = {
    "streaks": {
        "quality": "MEDIUM",
        "iterations": 3,
        "color_modulation": 0.25,
        "mix": 0.0,
        "threshold": 1.0,
        "streaks": 4,
        "angle_offset": 0.0,
        "fade": 0.8999999761581421
    },
    "bloom": {
        "quality": "MEDIUM",
        "mix": 0.0,
        "threshold": 1.0,
        "size": 8
    },
    "ghosts": {
        "quality": "MEDIUM",
        "iterations": 3,
        "color_modulation": 0.25,
        "mix": 0.0,
        "threshold": 1.0
    },
    "fog_glow": {
        "quality": "MEDIUM",
        "mix": 0.0,
        "threshold": 1.0,
        "size": 8
    },
    "simple_star": {
        "quality": "MEDIUM",
        "iterations": 3,
        "mix": 0.0,
        "threshold": 1.0,
        "fade": 0.8999999761581421,
        "use_rotate_45": True
    }
}
