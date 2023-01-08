from typing import List

class Achievement(object):

    name : str
    taskline_format : str
    custom_asset : str

    requirement : int
    prerequisites : List["Achievement"]

    def __init__(self, name : str, custom_asset : str, taskline_format : str, prerequisites : int):
        self.name = name
        self.taskline_format = taskline_format
        self.custom_asset = custom_asset
        self.prerequisites = prerequisites