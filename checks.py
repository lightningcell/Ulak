from discord.ext import commands
import utils
import discord


def app_command_has_permission(interaction: discord.Interaction):
    """
    Checks the author is owner or author in the accessible-roles.
    :return: Returns True or False
    """

    if interaction.user.id == interaction.guild.owner_id:
        return True

    guild_id = interaction.guild_id
    data = utils.get_guild_info(guild_id)
    accesible_role_ids = data['accessible-roles'].copy()
    user_role_ids = [str(role.id) for role in interaction.user.roles]

    if len(set(accesible_role_ids).intersection(set(user_role_ids))) >= 1:
        return True
    else:
        return False


def text_command_has_permission(ctx: commands.Context):
    """
    Checks the author is owner or author in the accessible-roles.
    :return: Returns True or False
    """

    if ctx.author.id == ctx.guild.owner_id:
        return True

    guild_id = ctx.guild.id
    data = utils.get_guild_info(guild_id)
    accesible_role_ids = data['accessible-roles'].copy()
    user_role_ids = [str(role.id) for role in ctx.author.roles]

    if len(set(accesible_role_ids).intersection(set(user_role_ids))) >= 1:
        return True
    else:
        return False
