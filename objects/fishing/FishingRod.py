class FishingRod(object):

    id : int
    name : str
    asset : str

    fishing_power : float = 1.0
    treasure_modifier : float = 0.0


    def __init__(
        self,
        id : int,
        name : str,
        asset : str,
        *,
        fishing_power : float = 1.0,
        treasure_modifier : float = 0.0
    ) -> None:
        self.id = id
        self.name = name
        self.asset = asset

        self.fishing_power = fishing_power
        self.treasure_modifier = treasure_modifier