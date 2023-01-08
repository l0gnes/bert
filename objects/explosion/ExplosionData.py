from datetime import datetime, timedelta
from .ExplosionReason import ExplosionReason
from .ExplosionWeather import ExplosionWeather
from discord.abc import User
from typing import Literal

class ExplosionData(object):

    time_exploded : datetime
    explosion_reason : ExplosionReason
    exploded_by : User
    score : int
    explosion_weather : str

    def __init__(
        self,
        time_exploded : datetime,
        score : int,
        exploded_by : User,
        *,
        explosion_reason : ExplosionReason = ExplosionReason.GENERIC_EXPLOSION,
        explosion_weather : ExplosionWeather
    ) -> None:
        self.time_exploded = time_exploded
        self.score = score
        self.explosion_reason = explosion_reason
        self.exploded_by = exploded_by
        self.explosion_weather = explosion_weather

    @property
    def delta(self) -> timedelta:
        return datetime.now() - self.time_exploded

    # Me < Other
    def __lt__(self, other : "ExplosionData") -> bool:
        return self.score < other.score

    # Me <= Other
    def __le__(self, other : "ExplosionData") -> bool:
        return self.score <= other.score

    # Me > Other
    def __gt__(self, other : "ExplosionData") -> bool:
        return self.score > other.score

    # Me >= Other
    def __ge__(self, other : "ExplosionData") -> bool:
        return self.score >= other.score