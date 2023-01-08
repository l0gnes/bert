
from discord import User
from discord.ext.commands.errors import BadArgument
from bert import BertBot
from objects.fishing.FishingRod import FishingRod
from objects.fishing.FishingAccount import FishingAccount
from typing import Union, Tuple, List
from objects.fishing.Fish import Fish
from objects.fishing.Junk import Junk
from objects.fishing.exceptions import FishingBagIsFull
from objects.fishing.FishLogicHandler import FishLogicHandler
from objects import EconomyManager

class FishingManager(object):

    ecoman : EconomyManager
    fishlog : FishLogicHandler

    fishing_rods = {
        0 : FishingRod(
            id = 0,
            name = "Simple Rod",
            asset = "SIMPLE_ROD",
            fishing_power=1.0,
            treasure_modifier=0.01
        ),
        1 : FishingRod(
            id = 1,
            name = "Better Rod",
            asset = "BETTER_ROD",
            fishing_power=1.25,
            treasure_modifier=0.025
        ),
        2 : FishingRod(
            id = 2,
            name = "Best Rod",
            asset = "BEST_ROD",
            fishing_power = 2.25,
            treasure_modifier = 0.075
        )
    }

    def __init__(self, client : "BertBot", *, fish_logic : FishLogicHandler = None) -> None:

        self.client = client
        self.ecoman = client.ecoman
        self.fishlog = fish_logic

    async def ensure_fishing_account(self, user : User) -> None:
        check = await self.client.pool.fetchrow(
            "SELECT * FROM fishing WHERE userid=$1", user.id
        )

        if not check:
            await self.client.pool.execute(
                "INSERT INTO fishing(userid) VALUES ($1)", user.id
            )

    async def fetch_partial_fishing_account(self, user : User, *, bypass_ensure : bool = False) -> FishingAccount:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        raw_account = await self.client.pool.fetchrow(
            "SELECT * FROM fishing WHERE userid=$1", user.id
        )

        return FishingAccount(
            user                = user,
            fishing_rod         = self.fishing_rods[raw_account['fishing_rod']],
            fish_caught         = raw_account['fish_caught'],
            experience          = raw_account['experience'],
            quests_completed    = raw_account['quests_completed'],
            treasure_fished     = raw_account['treasure_fished'],
            bag_level           = raw_account["bag_level"],
        )

    async def set_fishing_rod(
        self, 
        user : User, 
        rod : Union[FishingRod, int],
        *, 
        bypass_ensure : bool = False
    ) -> None:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        if isinstance(rod, int):
            rod = self.fishing_rods.get(rod, None)

            if rod is None:
                raise BadArgument("No fishing rod exists with that id")
                return

        await self.client.pool.execute(
            "UPDATE fishing SET fishing_rod=$1 WHERE userid=$2",
            rod.id, user.id
        )

    async def bag_is_full(
        self,
        user : User,
        *,
        bypass_ensure : bool = False
    ) -> bool:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        account = await self.fetch_partial_fishing_account(user, bypass_ensure=True)

        used_space = await self.client.pool.fetchval(
            "SELECT SUM(amount) AS TOTAL FROM caught_fish WHERE userid=$1",
            user.id
        )

        if used_space is None: used_space = 0
        return account.bag_size <= used_space

    async def bag_count_free_space(
        self,
        user : User,
        *,
        bypass_ensure : bool = False
    ) -> int:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        account = await self.fetch_partial_fishing_account(user, bypass_ensure=True)
        max_size = account.bag_size

        used_space = await self.client.pool.fetchval(
            "SELECT SUM(amount) AS TOTAL FROM caught_fish WHERE userid=$1",
            user.id
        )

        return max_size - (used_space if used_space is not None else 0)
            
    async def add_fish_to_bag(
        self,
        user : User,
        fish : Union[Junk, Fish],
        amount : int,
        *,
        bypass_ensure : bool = False
    ) -> None:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        bag_check = await self.bag_is_full(user, bypass_ensure=True)

        if bag_check: # If bag is full, raise an error
            raise FishingBagIsFull

        await self.client.pool.execute(
            """
            INSERT INTO caught_fish(userid, fishid, amount)
            VALUES ($1, $2, $3)
            ON CONFLICT ON CONSTRAINT userid_fishid DO
            UPDATE SET amount = EXCLUDED.amount + caught_fish.amount;
            """,
            user.id, fish.slug, amount
        )

    async def increment_fish_caught_statistic(
        self,
        user : User,
        amount : int,
        *,
        bypass_ensure : bool = False
    ) -> None:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        await self.client.pool.execute(
            "UPDATE fishing SET fish_caught = fish_caught + $1 WHERE userid=$2",
            amount, user.id
        )

    async def increment_fishing_experience(
        self,
        user : User,
        experience : int,
        *,
        bypass_ensure : bool = False
    ) -> None:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        await self.client.pool.execute(
            "UPDATE fishing SET experience = experience + $1 WHERE userid=$2",
            experience, user.id
        )

    async def reset_fish_caught_statistic(
        self,
        user : User,
        *,
        bypass_ensure : bool = False
    ) -> None:
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        await self.client.pool.execute(
            "UPDATE fishing SET fish_caught = 0 WHERE userid=$2", user.id
        )

    async def fetch_user_fish_bag(
        self, 
        user : User,
        *,
        bypass_ensure : bool = False
    ) -> List[Tuple[Union[Fish, Junk], int]]:
        
        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        rows = await self.client.pool.fetch(
            "SELECT fishid, amount FROM caught_fish WHERE userid=$1", user.id
        )

        fish_list = []

        for fish_record in rows:
            fish_list.append(
                (
                    self.fishlog.fetch_fish_from_slug(fish_record['fishid']),
                    fish_record['amount']
                )
            )

        return fish_list

    async def empty_user_fish_bag(
        self,
        user : User,
        *,
        bypass_ensure : bool = False
    ) -> None:

        if not bypass_ensure:
            await self.ensure_fishing_account(user)

        await self.client.pool.execute(
            "DELETE FROM caught_fish WHERE userid=$1", user.id
        )    