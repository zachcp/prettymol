from dataclasses import dataclass, replace, field, fields
from typing import List, Tuple
from .styles import StyleBase


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
