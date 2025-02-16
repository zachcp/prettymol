from dataclasses import dataclass, replace, field
from typing import Tuple, Optional
from .styles import StyleBase

class Light(StyleBase):
    """Provides all light properties available in Blender.

    See the Blender documentation for full details:
    https://docs.blender.org/manual/en/latest/render/lights/
    """
    type: str = field(default="POINT", metadata={"key": "Type"})  # POINT, SUN, SPOT, AREA
    color: Tuple[float, float, float] = field(default=(1.0, 1.0, 1.0), metadata={"key": "Color"})
    energy: float = field(default=100.0, metadata={"key": "Power"})
    diffuse: float = field(default=1.0, metadata={"key": "Diffuse"})
    specular: float = field(default=1.0, metadata={"key": "Specular"})
    volume: float = field(default=0.0, metadata={"key": "Volume"})
    shadow_soft_size: float = field(default=0.25, metadata={"key": "Shadow Soft Size"})

    # Spot light specific
    spot_size: float = field(default=0.785398, metadata={"key": "Spot Size"})  # 45 degrees in radians
    spot_blend: float = field(default=0.15, metadata={"key": "Spot Blend"})

    # Area light specific
    shape: str = field(default="SQUARE", metadata={"key": "Shape"})  # SQUARE, RECTANGLE, DISK, ELLIPSE
    size: float = field(default=0.25, metadata={"key": "Size"})
    size_y: Optional[float] = field(default=None, metadata={"key": "Size Y"})




class LightingCreator:
    def __init__(self):
        pass

    def new(self) -> Light:
        return Light()

    def key_light(self) -> Light:
        """Main light source, typically positioned above and to the side"""
        return replace(Light(),
            type="SUN",
            energy=5.0,
            color=(1.0, 0.95, 0.9),
            shadow_soft_size=0.5
        )

    def fill_light(self) -> Light:
        """Softer light to fill shadows"""
        return replace(Light(),
            type="AREA",
            energy=2.0,
            color=(0.9, 0.95, 1.0),
            size=2.0,
            shadow_soft_size=1.0
        )

    def rim_light(self) -> Light:
        """Backlight for edge definition"""
        return replace(Light(),
            type="SPOT",
            energy=3.0,
            color=(1.0, 1.0, 1.0),
            spot_size=1.0,
            spot_blend=0.2,
            shadow_soft_size=0.1
        )

    def ambient_occlusion(self) -> Light:
        """Soft ambient light"""
        return replace(Light(),
            type="AREA",
            shape="DISK",
            energy=1.0,
            color=(0.8, 0.8, 0.8),
            size=5.0,
            shadow_soft_size=2.0
        )

    def dramatic(self) -> Light:
        """High contrast spotlight"""
        return replace(Light(),
            type="SPOT",
            energy=10.0,
            color=(1.0, 0.95, 0.9),
            spot_size=0.5,
            spot_blend=0.1,
            shadow_soft_size=0.05
        )

    def soft_box(self) -> Light:
        """Studio-style soft box light"""
        return replace(Light(),
            type="AREA",
            shape="RECTANGLE",
            energy=3.0,
            size=2.0,
            size_y=3.0,
            shadow_soft_size=1.0
        )

    def three_point_setup(self) -> tuple[Light, Light, Light]:
        """Returns a classic three-point lighting setup"""
        return (
            self.key_light(),
            self.fill_light(),
            self.rim_light()
        )

    def studio_setup(self) -> tuple[Light, Light, Light, Light]:
        """Returns a four-point studio lighting setup"""
        return (
            self.soft_box(),
            replace(self.soft_box(), energy=2.0),
            self.rim_light(),
            self.ambient_occlusion()
        )

    def outdoor_daylight(self) -> tuple[Light, Light]:
        """Simulates outdoor daylight"""
        return (
            replace(self.key_light(),
                energy=10.0,
                color=(1.0, 0.98, 0.95)),
            replace(self.ambient_occlusion(),
                energy=2.0,
                color=(0.8, 0.9, 1.0))
        )
