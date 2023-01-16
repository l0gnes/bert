import datetime

from discord import (
    Embed,
    Member,
    Guild
)

__all__ = ["Tag"]

class Tag(object):

    tagman      : "TagManager"
    creatorid   : int
    guildid     : int
    title       : str
    content     : str
    imageurl    : str
    created_at  : int
    edited_at   : int


    def __init__(
        self,
        tagman : "TagManager",
        creatorid : int,
        guildid : int,
        title : str,
        content : str,
        imageurl : str,
        created_at : int,
        edited_at : int
    ) -> None:
        self.tagman = tagman
        self.creatorid = creatorid
        self.guildid = guildid
        self.title = title
        self.content = content
        self.imageurl = imageurl
        self.created_at = created_at
        self.edited_at = edited_at



    def get_guild(self) -> Guild:
        return self.tagman.client.get_guild(self.guildid)



    async def get_owner(self) -> Member:
        return await self.get_guild().fetch_member(self.creatorid)


    
    async def create_embed(self) -> Embed:

        owner = await self.get_owner()

        return Embed(
            colour = 0xFFFF00,
            title = self.title,
            description = self.content,
            timestamp = self.edited_at
        ).set_footer(
            text = "Tag Owner: %s#%s" % (
                owner.name, owner.discriminator
            ),
            icon_url = owner.display_avatar
        ).set_image(
            url = self.imageurl
        )