from discord import User
from objects.fishing.FishingRod import FishingRod

class FishingAccount(object):
    
    user : User
    fishing_rod : FishingRod
    fish_caught : int
    experience : int
    quests_completed : int
    treasure_fished : int
    bag_level : int

    def __init__(
        self,
        user : User,
        fishing_rod: FishingRod,
        fish_caught : int,
        experience : int,
        quests_completed : int,
        treasure_fished : int,
        bag_level : int
    ) -> None:
        self.user = user
        self.fishing_rod = fishing_rod
        self.fish_caught = fish_caught
        self.experience = experience
        self.quests_completed = quests_completed
        self.treasure_fished = treasure_fished
        self.bag_level = bag_level
        
    @property
    def level(self) -> int:
        return int(
            (self.experience / 50) ** (1 / 1.55)
        ) + 1

    @property
    def experience_to_next_level(self) -> float:
        """The level parameter can replace the next level"""
        return self.experience_for_level(self.level)

    def experience_for_level(self, level : int) -> float:
        return 50 * level ** 1.55

    @property
    def calculated_fishing_power(self) -> float:
        return self.fishing_rod.fishing_power + (0.35 * self.level)

    @property
    def bag_size(self) -> int:
        return (self.bag_level + 1) * 15 + (5 * (self.level - 1))

    def will_level_up_check(self, experience : int) -> bool:
        """Returns true if experience will level the user up"""
        return (self.experience + experience) >= self.experience_to_next_level