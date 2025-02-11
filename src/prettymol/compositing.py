from dataclasses import dataclass, replace, field, fields
from typing import List, Tuple
from .styles import StyleBase



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
