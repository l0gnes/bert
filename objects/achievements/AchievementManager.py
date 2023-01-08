from objects.achievements.Achievement import Achievement
from objects.achievements.AchievementProgress import AchievementProgress
from typing import List
from discord import User

__all__ = ["AchievementManager"]

class AchievementManager(object):

    client : "BertBot"
    is_setup : bool 

    achievement_cache : List[Achievement]

    def __init__(self, client : "BertBot") -> None:
        self.client = client

        self.achievement_cache = []
        self.is_setup = False

    async def setup(self) -> None:
        """Caches Achievement Definitions from the database"""
        ach_records = await self.client.pool.fetch(
            "SELECT * FROM achievements_def;"
        )

        for record in ach_records:
            self.achievement_cache.append(
                Achievement.from_record(record)
            )

        self.is_setup = True

    async def fetch_achievement_progress(
        self,
        user : User,
        achievement_id : str
    ) -> None:
        row = await self.client.pool.fetchrow(
            """
            SELECT 
                achievements.progress, achievement_defs.requirement 
            FROM achievements 
            INNER JOIN achievements_def ON 
                achievements.achievement = achievements_def.achievement_id 
            WHERE 
                achievements.userid=$1 
                AND 
                achievements_defs.achievement_id=$2 
            ; 
            """,
            (
                user.id, achievement_id
            )
        )

        if row == None:
            return None

        return AchievementProgress(
            progress = row["progress"],
            requirement = row["requirement"]
        )