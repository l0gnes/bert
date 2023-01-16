import discord
from discord import app_commands
from discord.ext import commands
from typing import List
from os import environ
import asyncpg
from objects.AssetMap import AssetMap
from objects.EconomyManager import EconomyManager
from objects.CommandTreeCacher import CommandTreeCacher
from objects.BertStatuses import BertStatus
from objects.achievements.AchievementManager import AchievementManager

import logging

__all__ = ["BertBot"]

class BertBot(commands.Bot):

    debug_servers : List[int]
    pool : asyncpg.Pool
    ecoman : EconomyManager
    achieveman : AchievementManager
    bert_status : BertStatus

    emoji_map : AssetMap
    asset_map : AssetMap

    logger : logging.Logger

    debug_mode : bool = False

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(
            intents=discord.Intents.all(),
            command_prefix=".", # Does nothing
        )

        self.debug_servers = (
            1020909558933237800,
        )

        self.developer_ids = (
            761057223362347008,
        )

        self.auto_load_cogs = (
            "cogs.number_guess",
            "cogs.dev",
            "cogs.eco",
            "cogs.leaderboard",
            "cogs.fishing",
            "cogs.achievements",
            "cogs.tags",
            #"cogs.cheese",
            #"cogs.test",
        )

        self.debug_mode = environ.get('DEBUG_MODE', 'false').lower() == 'true'

        self.bert_status = BertStatus(
            self, randomize=True
        )

        self.logger = logging.getLogger("discord")


    async def run_db_setup_script(self) -> None:
        
        with open("./schema.sql", 'r') as schema:
            data = schema.read()

            if data:
                await self.pool.execute(data)
        

    async def setup_hook(self) -> None:

        self.pool = await asyncpg.create_pool(environ["POSTGRES_URI"])
        await self.run_db_setup_script()

        self.asset_map = AssetMap.from_json('./asset_map.json')
        self.emoji_map = AssetMap.from_json('./emoji_map.json')

        self.ecoman = EconomyManager(self)

        self.achieveman = AchievementManager(client=self)
        await self.achieveman.setup()

        for cog in self.auto_load_cogs:

            try:
                await self.load_extension(cog)
                self.logger.debug("Loaded cog -> \"%s\"" % cog.upper())

            except Exception as err:
                print(err)

        ctc = CommandTreeCacher(self.tree)
        if ctc.tree_has_changes("./cached_cmd_tree.json", update_if_changed = True):

            self.logger.warning("CommandTreeCacher detected changes! Syncing command tree in debug guilds.")

            for guild_id in self.debug_servers:

                gObj = discord.Object(
                        id = guild_id
                    )

                self.tree.copy_global_to(
                    guild = gObj
                )

                await self.tree.sync(guild=gObj)

            self.logger.info("Command re-sync complete!")

        else:
            self.logger.info("CommandTreeCacher detected no changes in command tree.")

        self.add_listener(self.ready_hook, "on_ready")
        return await super().setup_hook()

    async def ready_hook(self) -> None:

        await self.wait_until_ready()

        await self.bert_status.nextPresence()

    
if __name__ == "__main__":

    from dotenv import load_dotenv

    load_dotenv()

    bert = BertBot()
    bert.run(
        environ.get("TOKEN")
    )