import typing
from os import PathLike
import json

class TieredAsset(object):
    
    tiers : typing.Tuple

    def __init__(self, *files) -> None:
        self.tiers = files

    def __iter__(self):
        yield from self.tiers

    def __getitem__(self, key : int):
        return self.tiers[key]


class AssetMap(object):

    assets : typing.Dict[str, typing.Union["TieredAsset", str]]

    def __init__(self) -> None:
        self.assets = {}

    def fetch_first(self, key : str) -> typing.Union[str, None]:
        # Returns the first asset if it exists
        if key in self.assets.keys():

            asset = self.assets[key]

            if isinstance(asset, TieredAsset):
                return asset[0]

            return asset

        return None

    def fetch_tiered(self, key : str) -> typing.Union[TieredAsset, str, None]:
        # Returns a tiered asset, If the asset is not tiered it will return a string in a list anyways
        if key in self.assets.keys():

            asset = self.assets[key]

            if isinstance(asset, str):
                return (asset,)
            
            return asset

        return None

    @classmethod
    def from_json(cls, file : PathLike) -> "AssetMap":
        
        with open(file, 'r') as f:
            data = json.load(f)

        newAssetMap = cls()

        for k, v in data.items():

            if isinstance(v, list):
                newAssetMap.assets[k] = TieredAsset(*v)
            else:
                newAssetMap.assets[k] = v

        return newAssetMap