from discord import User
from discord.ext import commands

class EconomyManager(object):

    client : commands.Bot

    def __init__(self, client : commands.Bot) -> None:
        self.client = client

    async def ensure_eco_account(self, user : User) -> None:
        check = await self.client.pool.fetchrow("SELECT * FROM economy WHERE userid=$1", user.id)
        if not check:
            await self.client.pool.execute(
                "INSERT INTO economy(userid, balance) VALUES ($1, 0)", (user.id)
            )

    async def get_balance(self, user : User, *, bypass_ensure : bool = False) -> int:
        if not bypass_ensure:
            await self.ensure_eco_account(user)
        
        balance = await self.client.pool.fetchval("SELECT balance FROM economy WHERE userid=$1", user.id)
        return balance

    async def set_balance(self, user : User, balance : int, *, bypass_ensure : bool = False) -> int:
        if not bypass_ensure:
            await self.ensure_eco_account(user)
        await self.client.pool.execute("UPDATE economy SET balance=$1 WHERE userid=$2", balance, user.id)

    async def add_balance(self, user : User, amount : int, *, bypass_ensure : bool = False) -> int:
        if not bypass_ensure:
            await self.ensure_eco_account(user)

        r = await self.client.pool.fetchrow(
            """UPDATE economy 
            SET balance=balance+$1 
            WHERE userid=$2 RETURNING balance;
            """
            , amount, user.id)

        return r['balance']

    async def deduct_balance(self, user : User, amount : int, *, bypass_ensure : bool = False) -> int:
        if not bypass_ensure:
            await self.ensure_eco_account(user)

        r = await self.client.pool.fetchrow(
            """UPDATE economy
            SET balance=balance-$1
            WHERE userid=$2 RETURNING balance
            """,
            amount, user.id
        )

        return r['balance']

    async def has_balance(self, user : User, amount : int, *, bypass_ensure : bool = False) -> bool:
        if not bypass_ensure:
            await self.ensure_eco_account(user)

        user_balance = await self.get_balance(user, bypass_ensure=True)

        return user_balance >= amount

    async def get_leaderboard(self) -> list:
        resp = await self.client.pool.fetch("SELECT * FROM economy WHERE balance>0 ORDER BY balance DESC;")
        return [(x['userid'], x['balance']) for x in resp]