from dataclasses import dataclass, replace, field, fields
from typing import List, Tuple


@dataclass(frozen=True)
class StyleBase:
    def get_by_key(self, original_key: str):
        for f in fields(self):
            if f.metadata.get('key') == original_key:
                return getattr(self, f.name)
        return None

@dataclass(frozen=True)
class BallStickStyle(StyleBase):
    style: str = field(default="ball+stick", metadata={"key": "Style"})
    quality: int = field(default=2, metadata={"key": "Quality"})
    as_mesh: bool = field(default=True, metadata={"key": "As Mesh"})
    sphere_radii: float = field(default=0.3, metadata={"key": "Sphere Radii"})
    bond_split: bool = field(default=False, metadata={"key": "Bond Split"})
    bond_find: bool = field(default=False, metadata={"key": "Bond Find"})
    bond_radius: float = field(default=0.3, metadata={"key": "Bond Radius"})
    color_blur: bool = field(default=False, metadata={"key": "Color Blur"})
    shade_smooth: bool = field(default=True, metadata={"key": "Shade Smooth"})


@dataclass(frozen=True)
class CartoonStyle(StyleBase):
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


@dataclass(frozen=True)
class RibbonStyle(StyleBase):
    style: str = field(default="ribbon", metadata={"key": "Style"})
    quality: int = field(default=3, metadata={"key": "Quality"})
    radius: float = field(default=1.6, metadata={"key": "Radius"})
    smoothing: float = field(default=0.6, metadata={"key": "Smoothing"})
    color_blur: bool = field(default=False, metadata={"key": "Color Blur"})
    shade_smooth: bool = field(default=False, metadata={"key": "Shade Smooth"})

@dataclass(frozen=True)
class SpheresStyle(StyleBase):
    style: str = field(default="sphere", metadata={"key": "Style"})
    as_mesh: bool = field(default=True, metadata={"key": "As Mesh"})
    radii: float = field(default=0.8, metadata={"key": "Radii"})
    subdivisions: int = field(default=2, metadata={"key": "Subdivisions"})
    shade_smooth: bool = field(default=False, metadata={"key": "Shade Smooth"})


@dataclass(frozen=True)
class SticksStyle(StyleBase):
    style: str = field(default="stick", metadata={"key": "Style"})
    quality: int = field(default=2, metadata={"key": "Quality"})
    radius: float = field(default=0.2, metadata={"key": "Radius"})
    color_blur: bool = field(default=False, metadata={"key": "Color Blur"})
    shade_smooth: bool = field(default=False, metadata={"key": "Shade Smooth"})


@dataclass(frozen=True)
class SurfaceStyle(StyleBase):
    style: str = field(default="surface", metadata={"key": "Style"})
    quality: int = field(default=3, metadata={"key": "Quality"})
    separate: bool = field(default=True, metadata={"key": "Separate"})
    attribute: str = field(default="chain_id", metadata={"key": "Attribute"})
    scale_radii: float = field(default=1.5, metadata={"key": "Scale Radii"})
    probe_size: float = field(default=1.0, metadata={"key": "Probe Size"})
    triangulate: bool = field(default=False, metadata={"key": "Triangulate"})
    relaxation_steps: int = field(default=10, metadata={"key": "Relaxation Steps"})
    by_ca: bool = field(default=False, metadata={"key": "by CA"})
    blur: int = field(default=2, metadata={"key": "Blur"})
    shade_smooth: bool = field(default=True, metadata={"key": "Shade Smooth"})



@dataclass(frozen=True)
class BSDFPrincipled(StyleBase):
    base_color: Tuple[float, float, float, float] = field(default=(0.8, 0.8, 0.8, 1.0), metadata={"key": "Base Color"})
    metallic: float = field(default=0.0, metadata={"key": "Metallic"})
    roughness: float = field(default=0.2, metadata={"key": "Roughness"})
    ior: float = field(default=1.45, metadata={"key": "IOR"})
    alpha: float = field(default=1.0, metadata={"key": "Alpha"})
    normal: Tuple[float, float, float] = field(default=(0.0, 0.0, 0.0), metadata={"key": "Normal"})
    weight: float = field(default=0.0, metadata={"key": "Weight"})
    diffuse_roughness: float = field(default=0.0, metadata={"key": "Diffuse Roughness"})
    subsurface_weight: float = field(default=0.0, metadata={"key": "Subsurface Weight"})
    subsurface_radius: Tuple[float, float, float] = field(default=(1.0, 0.2, 0.1), metadata={"key": "Subsurface Radius"})
    subsurface_scale: float = field(default=0.05, metadata={"key": "Subsurface Scale"})
    subsurface_ior: float = field(default=1.4, metadata={"key": "Subsurface IOR"})
    subsurface_anisotropy: float = field(default=0.0, metadata={"key": "Subsurface Anisotropy"})
    specular_ior_level: float = field(default=0.5, metadata={"key": "Specular IOR Level"})
    specular_tint: Tuple[float, float, float, float] = field(default=(1.0, 1.0, 1.0, 1.0), metadata={"key": "Specular Tint"})
    anisotropic: float = field(default=0.0, metadata={"key": "Anisotropic"})
    anisotropic_rotation: float = field(default=0.0, metadata={"key": "Anisotropic Rotation"})
    tangent: Tuple[float, float, float] = field(default=(0.0, 0.0, 0.0), metadata={"key": "Tangent"})
    transmission_weight: float = field(default=0.0, metadata={"key": "Transmission Weight"})
    coat_weight: float = field(default=0.0, metadata={"key": "Coat Weight"})
    coat_roughness: float = field(default=0.03, metadata={"key": "Coat Roughness"})
    coat_ior: float = field(default=1.5, metadata={"key": "Coat IOR"})
    coat_tint: Tuple[float, float, float, float] = field(default=(1.0, 1.0, 1.0, 1.0), metadata={"key": "Coat Tint"})
    coat_normal: Tuple[float, float, float] = field(default=(0.0, 0.0, 0.0), metadata={"key": "Coat Normal"})
    sheen_weight: float = field(default=0.0, metadata={"key": "Sheen Weight"})
    sheen_roughness: float = field(default=0.5, metadata={"key": "Sheen Roughness"})
    sheen_tint: Tuple[float, float, float, float] = field(default=(0.5, 0.5, 0.5, 1.0), metadata={"key": "Sheen Tint"})
    emission_color: Tuple[float, float, float, float] = field(default=(0.0, 0.0, 0.0, 1.0), metadata={"key": "Emission Color"})
    emission_strength: float = field(default=0.0, metadata={"key": "Emission Strength"})
    thin_film_thickness: float = field(default=0.0, metadata={"key": "Thin Film Thickness"})
    thin_film_ior: float = field(default=1.3, metadata={"key": "Thin Film IOR"})



@dataclass(frozen=True)
class GlareStreaks(StyleBase):
    quality: str = field(default="MEDIUM", metadata={"key": "quality"})
    iterations: int = field(default=3, metadata={"key": "iterations"})
    color_modulation: float = field(default=0.25, metadata={"key": "color_modulation"})
    mix: float = field(default=0.0, metadata={"key": "mix"})
    threshold: float = field(default=1.0, metadata={"key": "threshold"})
    streaks: int = field(default=4, metadata={"key": "streaks"})
    angle_offset: float = field(default=0.0, metadata={"key": "angle_offset"})
    fade: float = field(default=0.9, metadata={"key": "fade"})



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
