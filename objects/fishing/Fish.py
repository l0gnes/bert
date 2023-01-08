class Fish(object):

    name : str
    asset : str
    value : int
    min_power : float

    def __init__(self, name : str, asset : str, value : int, min_power : float) -> None:
        self.name = name
        self.asset = asset
        self.value = value
        self.min_power = min_power

    @property
    def slug(self) -> str:
        return "fish_" + self.name.lower().replace(' ', '_')