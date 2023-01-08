from enum import Enum, auto

__all__ = [
    "ExplosionReason"
]

class ExplosionReason(Enum):

    GENERIC_EXPLOSION = auto()
    TOO_WINDY = auto()
    BAD_TIME = auto()
    TOO_HUMID = auto()
    BAD_WIND_DIRECTION = auto()
    TOO_COLD = auto()
    TOO_HOT = auto()
    STARVATION_IMPLOSION = auto()