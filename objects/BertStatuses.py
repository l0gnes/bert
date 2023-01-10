from discord import Client, ActivityType, Activity, Status
from typing import List, Tuple, Set, Optional
from random import choice

class BertStatus(object):

    presence_list : List[Tuple[str, ActivityType, Status]] = [
        ("in a thimble", ActivityType.playing, Status.online),
        ("sleepy music", ActivityType.listening, Status.online),
        ("competitive shitting", ActivityType.competing, Status.online),
        ("with some twigs", ActivityType.playing, Status.online),
        ("minecraft (rat edition)", ActivityType.playing, Status.online),
        ("stewart little", ActivityType.watching, Status.online),
        ("penis music", ActivityType.listening, Status.online),
        ("in the road", ActivityType.playing, Status.online),
        ("with legos!", ActivityType.playing, Status.online),
        ("the intrusive thoughts", ActivityType.listening, Status.online),
        ("the world burn", ActivityType.watching, Status.online),
        ("in the sink", ActivityType.playing, Status.online),
        ("with belly button lint", ActivityType.playing, Status.online)
    ]

    debug_status_enabled : bool = True # Whether or not to use a debug status if the bot is in debug mode
    debug_status : Tuple[str, ActivityType, Status] = (
        "myself be developed", ActivityType.watching, Status.idle
    )

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
        
        if not self.randomize and not (self.debug_status_enabled and self.client.debug_mode):

            self.current_index = self.fetch_valid_next_index()
            name, type, status = self.presence_list[new_presence]

            return await self.client.change_presence(
                activity = Activity(
                    name = name,
                    type = type
                ),
                status = status
            )

        if self.debug_status_enabled and self.client.debug_mode:

            return await self.client.change_presence(
                activity = Activity(
                    name = self.debug_status[0],
                    type = self.debug_status[1]
                ),
                status = self.debug_status[2]
            )

        name, type, status = self.get_random_presence_index()

        return await self.client.change_presence(
            activity = Activity(
                name = name,
                type = type
            ),
            status = status
        )