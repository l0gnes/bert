from typing import Union, Optional
from discord import Member, User, Guild
from bert import BertBot

from objects.tags.Tag import Tag
from objects.tags.TagErrors import (
    TitleAlreadyInUse,
    UserContextLacksGuild,
    TagDoesNotExist
)

class TagManager(object):

    client : BertBot

    def __init__(self, client : BertBot) -> None:
        self.client = client



    async def ensure_tag_exists(
        self,
        guild : Guild,
        title : str
    ) -> bool:

        check = await self.client.pool.fetchval(
            """
            SELECT title FROM tags 
            WHERE
                guildid = $1 AND title = $2;   
            """,
            guild.id, title.lower()
        )

        return check is not None



    @staticmethod
    def ensure_guild_attr(
        user : Union[Member, User]
    ) -> bool:
        return hasattr(user, "guild")



    async def ensure_user_owns_tag(
        self,
        user : Union[Member, User],
        title : str,
        *,
        guild : Optional[Guild] = None
    ):

        if not self.ensure_guild_attr(user) and guild is None:
            raise UserContextLacksGuild()

        elif guild is None:
            guild = user.guild

        check = await self.client.pool.fetchval(
            """
                SELECT (title) 
                FROM tags
                WHERE
                    creatorid=$1 AND
                    guildid=$2 AND
                    title=$3;
            """,
            user.id, guild.id, title.lower()
        )

        return check is not None



    async def create_new_tag(
        self,
        owner : Union[Member, User],
        title : str,
        content : str,
        *,
        image_url : Optional[str] = None,
        guild : Optional[Guild] = None,
        overwrite : bool = False
    ) -> None:

        if not hasattr(owner, "guild") and guild is None:
            raise UserContextLacksGuild(
                """Passed argument is of type user and hence has no reference to the guild object. 
                Please pass the correct value, or alternatively, pass the guild kwarg."""
                )

        if guild is None:
            guild = owner.guild

        check = await self.ensure_tag_exists(
            title = title,
            guild = guild
        )
        
        if check:
            raise TitleAlreadyInUse(
                """
                Tag with already exists in guild, please use a different title.
                """
            )
        

        await self.client.pool.execute(
            """INSERT INTO 
                tags(creatorid, guildid, title, content, imageurl)
            VALUES
                ($1, $2, $3, $4, $5); 
            """,
            owner.id, guild.id,
            title, content, image_url
        )



    async def update_tag(
        self,
        guild : Guild,
        title : str,
        *,
        owner : Union[Member, User] = None,
        content : str = None,
        image_url : str = None
    ) -> None:

        print('in')

        check = await self.ensure_tag_exists(
            guild, title
        )

        print("a")

        if not check:
            raise TagDoesNotExist(
                """
                Tag does not exist, cannot update attributes of non-existent tag (dumbass)
                """
            )

        print("b")

        await self.client.pool.execute(
            """
            UPDATE tags SET
                creatorid = COALESCE($1, creatorid),
                content = COALESCE($2, content),
                imageurl = COALESCE($3, imageurl),
                edited_at = CURRENT_TIMESTAMP
            WHERE
                guildid = $4 AND title = $5
            """,
            None if owner is None else owner.id,
            content,
            image_url,
            guild.id,
            title
        )

        print("c")


    async def delete_tag(
        self,
        owner : Union[Member, User],
        title : str,
        *,
        guild : Guild = None,
    ) -> None:

        if self.ensure_guild_attr(owner) and guild is None:
            raise UserContextLacksGuild()

        if guild is None:
            guild = owner.guild

        await self.client.pool.execute(
            "DELETE FROM tags WHERE guildid=$1 AND creatorid=$2 AND title=$3",
            guild.id, owner.id, title
        )

    

    async def fetch_tag_by_title(
        self,
        guild : Guild,
        title : str
    ) -> Tag | None:
        
        row = await self.client.pool.fetchrow(
            """
            SELECT 
                (creatorid, guildid, title, content, imageurl, created_at, edited_at)
            FROM tags WHERE 
                guildid=$1 AND title=$2
            """,
            guild.id, title
        )

        if row is None: return None

        return Tag(
            self,
            row['row'][0],
            row['row'][1],
            row['row'][2],
            row['row'][3],
            row['row'][4],
            row['row'][5],
            row['row'][6]
        )



        
        

        