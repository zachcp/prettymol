from dataclasses import dataclass, replace, field, fields
from typing import List, Tuple


@dataclass(frozen=True)
class BallStickStyle:
    style: str = "ball+stick"
    quality: int = 2
    as_mesh: bool = True
    sphere_radii: float = 0.3
    bond_split: bool = False
    bond_find: bool = False
    bond_radius: float = 0.3
    color_blur: bool = False
    shade_smooth: bool = True

@dataclass(frozen=True)
class CartoonStyle:
    style: str = field(default="cartoon", metadata={"key": "Style"})
    quality: int = field(default=2, metadata={"key": "Quality"})
    dssp: bool = field(default=False, metadata={"key": "DSSP"})
    cylinders: bool = field(default=False, metadata={"key": "Cylinders"})
    arrows: bool = field(default=True, metadata={"key": "Arrows"})
    rounded: bool = field(default=False, metadata={"key": "Rounded"})
    thickness: float = field(default=0.6, metadata={"key": "Thickness"})
    width: float = field(default=2.2, metadata={"key": "Width"})
    loop_radius: float = field(default=0.3, metadata={"key": "Loop Radius"})
    smoothing: float = field(default=0.5, metadata={"key": "Smoothing"})
    color_blur: bool = field(default=False, metadata={"key": "Color Blur"})
    shade_smooth: bool = field(default=True, metadata={"key": "Shade Smooth"})

    def get_by_key(self, original_key: str):
        for f in fields(self):
            if f.metadata.get('key') == original_key:
                return getattr(self, f.name)
        return None

@dataclass(frozen=True)
class RibbonStyle:
    style: str = "ribbon"
    quality: int = 3
    radius: float = 1.6
    smoothing: float = 0.6
    color_blur: bool = False
    shade_smooth: bool = False

@dataclass(frozen=True)
class SpheresStyle:
    style: str = "sphere"
    as_mesh: bool = True
    radii: float = 0.8
    subdivisions: int = 2
    shade_smooth: bool = False

@dataclass(frozen=True)
class SticksStyle:
    style: str = "stick"
    quality: int = 2
    radius: float = 0.2
    color_blur: bool = False
    shade_smooth: bool = False

@dataclass(frozen=True)
class SurfaceStyle:
    style: str = "surface"
    quality: int = 3
    separate: bool = True
    attribute: str = "chain_id"
    scale_radii: float = 1.5
    probe_size: float = 1.0
    triangulate: bool = False
    relaxation_steps: int = 10
    by_ca: bool = False
    blur: int = 2
    shade_smooth: bool = True

@dataclass(frozen=True)
class BSDFPrincipled:
    base_color: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)
    metallic: float = 0.0
    roughness: float = 0.2
    ior: float = 1.45
    alpha: float = 1.0
    normal: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    weight: float = 0.0
    diffuse_roughness: float = 0.0
    subsurface_weight: float = 0.0
    subsurface_radius: Tuple[float, float, float] = (1.0, 0.2, 0.1)
    subsurface_scale: float = 0.05
    subsurface_ior: float = 1.4
    subsurface_anisotropy: float = 0.0
    specular_ior_level: float = 0.5
    specular_tint: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    anisotropic: float = 0.0
    anisotropic_rotation: float = 0.0
    tangent: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    transmission_weight: float = 0.0
    coat_weight: float = 0.0
    coat_roughness: float = 0.03
    coat_ior: float = 1.5
    coat_tint: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    coat_normal: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    sheen_weight: float = 0.0
    sheen_roughness: float = 0.5
    sheen_tint: Tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0)
    emission_color: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    emission_strength: float = 0.0
    thin_film_thickness: float = 0.0
    thin_film_ior: float = 1.3

@dataclass(frozen=True)
class GlareStreaks:
    quality: str = "MEDIUM"
    iterations: int = 3
    color_modulation: float = 0.25
    mix: float = 0.0
    threshold: float = 1.0
    streaks: int = 4
    angle_offset: float = 0.0
    fade: float = 0.9

@dataclass(frozen=True)
class GlareBloom:
    quality: str = "MEDIUM"
    mix: float = 0.0
    threshold: float = 1.0
    size: int = 8

@dataclass(frozen=True)
class GlareGhosts:
    quality: str = "MEDIUM"
    iterations: int = 3
    color_modulation: float = 0.25
    mix: float = 0.0
    threshold: float = 1.0

@dataclass(frozen=True)
class GlareFogGlow:
    quality: str = "MEDIUM"
    mix: float = 0.0
    threshold: float = 1.0
    size: int = 8

@dataclass(frozen=True)
class GlareSimpleStar:
    quality: str = "MEDIUM"
    iterations: int = 3
    mix: float = 0.0
    threshold: float = 1.0
    fade: float = 0.8999999761581421
    use_rotate_45: bool = True
