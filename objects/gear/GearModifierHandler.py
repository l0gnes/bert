from typing import Dict, Optional, Union
from OBJ.GearDefinition import GearDefinition

class GearModifier(object):
    slug : str
    prefix : Optional[str] = ""
    suffix : Optional[str] = ""

    strength : float = 0
    defence : float = 0
    crit_chance : float = 0

    def format_gear_title(self, gear : GearDefinition) -> str:
        tmp = gear.name

        if len(self.prefix) > 0:
            tmp = self.prefix + " " + tmp

        if len(self.suffix) > 0:
            tmp += " %s" % (self.suffix)

        return tmp

    def __init__(
        self,
        slug : str,
        *,
        prefix : str = "",
        suffix : str = "",
        strength : float = 0.0,
        defence : float = 0.0,
        crit_chance : float= 0.0
    ) -> None:
        self.slug = slug
        self.prefix = prefix
        self.suffix = suffix
        self.strength = strength
        self.defence = defence
        self.crit_chance = crit_chance

class GearModifierHandler(object):
    gear_modifiers : Dict[str, GearModifier] = {
        "might" : GearModifier(
            slug="might",
            suffix="of Might",
            strength=5.0
        ),
        "tank" : GearModifier(
            slug="tank",
            suffix="of the Tank",
            defence=5.0
        ),
        "sharp" : GearModifier(
            slug="sharp",
            prefix="Sharp",
            crit_chance=2.5
        ),
        "gilded" : GearModifier(
            slug="gilded",
            prefix="Gilded",
            crit_chance=7.5,
            defence=12.5,
            strength=20.0
        )
    }

    def find_modifier(self, key : str) -> Union[GearModifier, None]:
        return self.gear_modifiers.get(
            key, None
        )