from discord.ext import commands
import utils


def has_permission():
    def predicate(ctx: commands.Context):
        """
        Checks the author is owner or author in the accessible-roles.
        :param ctx: discord.ext.commands.Context (default value)
        :return: Returns True or False
        """
        if ctx.author.id == ctx.guild.owner_id:
            return True

        guild_id = ctx.guild.id
        data = utils.get_guild_info(guild_id)

        if len(set([str(r.id) for r in ctx.author.roles]).intersection(set(data["accessible-roles"]))) >= 1:
            return True
        else:
            return False

    return commands.check(predicate)
