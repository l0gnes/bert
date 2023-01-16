from discord.ext.commands.errors import CommandError

class UserContextLacksGuild(CommandError):
    pass

class TitleAlreadyInUse(CommandError):
    pass 

class TagDoesNotExist(CommandError):
    pass