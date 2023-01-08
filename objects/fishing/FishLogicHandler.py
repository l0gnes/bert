from typing import Union, Tuple, List, Literal, Optional
from objects.fishing.FishingAccount import FishingAccount
from objects.fishing.Fish import Fish
from objects.fishing.Junk import Junk
from objects.fishing.SpecialFishEvent import SpecialFishEvent

import json
import random

class FishLogicHandler(object):

    fish_list : List[Fish]
    junk_list : List[Junk]

    junk_threshold : int = 10

    def __init__(self):
        self.load_lists()

    def load_lists(self) -> None:

        with open("./objects/fishing/fishing_table.json") as fish_json:
            fish_json_data = json.load(fish_json)
        
        self.fish_list = [Fish(**f) for f in fish_json_data]

        with open("./objects/fishing/junk_table.json") as junk_json:
            junk_json_data = json.load(junk_json)

        self.junk_list = [Junk(**j) for j in junk_json_data]

    def fetch_fish_from_slug(self, slug : str) -> Union[Fish, Junk, None]:
        
        dict_to_search = None

        if slug.startswith("fish_"):
            dict_to_search = self.fish_list

        elif slug.startswith("junk_"):
            dict_to_search = self.junk_list


        if dict_to_search is None:
            raise ValueError("Invalid slug prefix??")

        search = list(
            filter(
                lambda f: f.slug == slug, dict_to_search
            )
        )

        # No Junk/Fish Found
        if len(search) == 0:
            return None

        return search[0]


    def catch_fish(self, fishingUser : FishingAccount, *, force_catch : Optional[Literal["JUNK", "FISH"]] = None) -> Tuple[int, Union[Fish, Junk]]:

        catchable_fish = list(
            filter(
                lambda f: f.min_power <= fishingUser.calculated_fishing_power,
                self.fish_list
            )
        )

        junk_chance = self.junk_threshold - (fishingUser.calculated_fishing_power + fishingUser.level)
        if junk_chance < 1: junk_chance = 1 # Fail-safe for junk chance

        fish_chance = (len(catchable_fish) * junk_chance) * fishingUser.fishing_rod.fishing_power

        winning_choice = random.choices(
            ("FISH", "JUNK"),
            weights = (fish_chance, junk_chance),
            k = 1
        )[0]

        if winning_choice == "FISH" or force_catch == "FISH":
            return random.choices(
                range(1, int(fishingUser.calculated_fishing_power)),
                [1 / i**(0.15*i) for i in range(1, int(fishingUser.calculated_fishing_power))],
                k = 1
            )[0], random.choices(
                catchable_fish,
                [100 - (f.min_power * 4) for f in catchable_fish],
                k = 1
            )[0]

        elif winning_choice == "JUNK" or force_catch == "JUNK":
            return 1, random.choice(self.junk_list)

    def calculate_experience_earned(
        self,
        fishingUser : FishingAccount,
        fish_type : Union[Fish, Junk],
        amount : int
    ) -> int:
        return max(
            1, 
            int(
            (fish_type.value * amount)  * fishingUser.fishing_rod.fishing_power
        ))

    def calculate_bag_value(
        self,
        bag : List[Tuple[Union[Fish, Junk], int]]
    ) -> int:
        ind_values = [amount * fish.value for fish, amount in bag]
        return sum(ind_values)

    def special_events_hook(
        self
    ) -> Union[SpecialFishEvent, None]:
        return random.choices(
            (None, SpecialFishEvent.CRITICAL_HOOK, SpecialFishEvent.DABLOON_DIVE),
            (99, 1, 1),
            k = 1
        )[0]