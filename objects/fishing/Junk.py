class Junk(object):

    name : str
    asset : str
    value : int

    def __init__(self, name : str, asset : str, value : int) -> None:
        self.name = name
        self.asset = asset
        self.value = value

    @property
    def slug(self) -> str:
        return "junk_" + self.name.lower().replace(' ', '_')