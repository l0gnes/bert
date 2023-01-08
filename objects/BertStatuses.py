from discord import Client, ActivityType, Activity
from typing import List, Tuple, Set
from random import choice

class BertStatus(object):

    presence_list : List[Tuple[str, ActivityType]] = [
        ("in a thimble", ActivityType.playing),
        ("sleepy music", ActivityType.listening),
        ("competitive shitting", ActivityType.competing),
        ("with some twigs", ActivityType.playing),
        ("minecraft (rat edition)", ActivityType.playing),
        ("stewart little", ActivityType.watching),
        ("penis music", ActivityType.listening),
        ("in the road", ActivityType.playing),
        ("with legos!", ActivityType.playing),
        ("the intrusive thoughts", ActivityType.listening),
        ("the world burn", ActivityType.watching),
        ("in the sink", ActivityType.playing),
        ("with belly button lint", ActivityType.playing)
    ]

    current_index : int
    randomize : bool
    randomize_cache : Set[Tuple[str, ActivityType]]

    def __init__(
        self, 
        client : Client, 
        *, 
        offset : int = 0,
        randomize : bool = False
    ) -> None:
        self.client = client
        self.current_index = offset
        self.randomize = randomize
        self.randomize_cache = set()

    def fetch_valid_next_index(self) -> int:

        if len(self.presence_list) <= self.current_index or self.current_index < 0:
            return 0

        return int(self.current_index + 1)

    def ensure_random_selection_possible(self) -> None:

        if len(set(self.presence_list).difference(self.randomize_cache)) < 1:
            self.randomize_cache.clear()

    def get_random_presence_index(self) -> Tuple[str, ActivityType]:

        diff = set(self.presence_list).difference(self.randomize_cache)

        selection = choice(list(diff))
        self.randomize_cache.add(selection)

        return selection

    async def nextPresence(self) -> None:

        new_presence = None
        
        if not self.randomize:

            self.current_index = self.fetch_valid_next_index()
            name, type = self.presence_list[new_presence]

            return await self.client.change_presence(
                activity = Activity(
                    name = name,
                    type = type
                )
            )

        name, type = self.get_random_presence_index()

        return await self.client.change_presence(
            activity = Activity(
                name = name,
                type = type
            )
        )