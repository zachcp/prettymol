from dataclasses import dataclass, replace, field
from typing import Tuple, Optional
from .styles import StyleBase



@dataclass(frozen=True)
class BaseLightProperties(StyleBase):
    """Base properties common to all light types"""
    color: Tuple[float, float, float] = field(default=(1.0, 1.0, 1.0), metadata={"key": "Color"})
    energy: float = field(default=100.0, metadata={"key": "Power"})
    diffuse: float = field(default=1.0, metadata={"key": "Diffuse"})
    specular: float = field(default=1.0, metadata={"key": "Specular"})
    volume: float = field(default=0.0, metadata={"key": "Volume"})

@dataclass(frozen=True)
class PointLight(BaseLightProperties):
    """Point light properties

    Omnidirectional light source that emits light equally in all directions
    """
    shadow_soft_size: float = field(default=0.25, metadata={"key": "Shadow Soft Size"})
    use_custom_distance: bool = field(default=False, metadata={"key": "Use Custom Distance"})
    custom_distance: float = field(default=40.0, metadata={"key": "Custom Distance"})

@dataclass(frozen=True)
class SunLight(BaseLightProperties):
    """Sun light properties

    Parallel rays from a distant source, with infinite range
    """
    angle: float = field(default=0.009, metadata={"key": "Angle"})  # Default is ~0.526 degrees

@dataclass(frozen=True)
class SpotLight(BaseLightProperties):
    """Spot light properties

    Cone-shaped light source
    """
    shadow_soft_size: float = field(default=0.25, metadata={"key": "Shadow Soft Size"})
    spot_size: float = field(default=0.785398, metadata={"key": "Spot Size"})  # 45 degrees in radians
    spot_blend: float = field(default=0.15, metadata={"key": "Spot Blend"})
    show_cone: bool = field(default=False, metadata={"key": "Show Cone"})
    use_custom_distance: bool = field(default=False, metadata={"key": "Use Custom Distance"})
    custom_distance: float = field(default=40.0, metadata={"key": "Custom Distance"})

@dataclass(frozen=True)
class AreaLight(BaseLightProperties):
    """Area light properties

    Light emitted from a surface with a specified shape
    """
    shape: Literal["SQUARE", "RECTANGLE", "DISK", "ELLIPSE"] = field(
        default="SQUARE",
        metadata={"key": "Shape"}
    )
    size: float = field(default=0.25, metadata={"key": "Size"})
    size_y: float = field(default=0.25, metadata={"key": "Size Y"})

class LightingCreator:
    def __init__(self):
        pass

    def point_light() -> PointLight:
        return PointLight()

    def sun_light() -> SunLight:
        return SunLight()

    def spot_light() -> SpotLight:
        return SpotLight()

    def area_light() -> AreaLight:
        return AreaLight()

    def key_light() -> SpotLight:
        """Main light source, typically positioned above and to the side"""
        return SpotLight().update_style(
            energy=5.0,
            color=(1.0, 0.95, 0.9),
            shadow_soft_size=0.5,
            spot_size=1.0,
            spot_blend=0.2
        )

    def fill_light() -> AreaLight:
        """Softer light to fill shadows"""
        return AreaLight().update_style(
            energy=2.0,
            color=(0.9, 0.95, 1.0),
            size=2.0,
            shape="RECTANGLE",
            size_y=3.0
        )

    def rim_light() -> SpotLight:
        """Backlight for edge definition"""
        return SpotLight().update_style(
            energy=3.0,
            color=(1.0, 1.0, 1.0),
            spot_size=0.8,
            spot_blend=0.2,
            shadow_soft_size=0.1
        )

    def outdoor_sun(self) -> SunLight:
        """Simulates outdoor sunlight"""
        return SunLight().update_style(
            energy=10.0,
            color=(1.0, 0.98, 0.95),
            angle=0.005
        )

    # def three_point_setup(self) -> tuple[SpotLight, AreaLight, SpotLight]:
    #     """Returns a classic three-point lighting setup"""
    #     return (
    #         self.key_light(),
    #         self.fill_light(),
    #         self.rim_light()
    #     )

    # def studio_setup(self) -> tuple[AreaLight, AreaLight, SpotLight, PointLight]:
    #     """Returns a four-point studio lighting setup"""
    #     main_light = AreaLight(
    #         energy=5.0,
    #         size=2.0,
    #         size_y=3.0,
    #         shape="RECTANGLE"
    #     )

    #     fill = AreaLight(
    #         energy=2.0,
    #         size=2.0,
    #         size_y=3.0,
    #         shape="RECTANGLE",
    #         color=(0.9, 0.95, 1.0)
    #     )

    #     rim = self.rim_light()

    #     ambient = PointLight(
    #         energy=1.0,
    #         color=(0.8, 0.8, 0.8),
    #         shadow_soft_size=2.0
    #     )

    #     return (main_light, fill, rim, ambient)
