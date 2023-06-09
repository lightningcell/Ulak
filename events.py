from discord.ext import commands
from discord import app_commands
import typing
import settings
import utils
import discord


class UlakEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def p_on_guild_join(guild: discord.Guild):
        """
        Saves the guild data and send message to the system channel of guild.
        """
        data = utils.get_base_data(guild.preferred_locale)
        utils.add_guild(guild.id)
        await guild.system_channel.send("@everyone" + "\n" + data["on_guild_join"])

    @staticmethod
    async def p_on_guild_remove(guild: discord.Guild):
        """
        Removes the guild data. Sends DM to the owner, if owner DM is open.
        """
        data = utils.get_base_data(guild.preferred_locale)
        try:
            utils.remove_guild(guild.id)
            await guild.owner.send(data["on_guild_remove"])
        except discord.errors.Forbidden:
            pass

    @staticmethod
    async def p_on_member_join(member: discord.Member):
        """
        Greetings member and sends messages to the admin-channels that set with commands
        """
        message = utils.get_base_data(member.guild.preferred_locale)["on_member_join"]
        mention = member.mention
        admin_channels = utils.get_guild_info(member.guild.id)['admin-channel-ids']

        await member.guild.system_channel.send(f"{mention}\n{message}")

        for _id in admin_channels:
            channel = discord.utils.get(member.guild.channels, id=int(_id))
            await channel.send(
                utils.get_base_data(member.guild.preferred_locale)["on_member_join_v2"] + "\n" + mention)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await UlakEvents.p_on_guild_join(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await UlakEvents.p_on_guild_remove(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await UlakEvents.p_on_member_join(member)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.message.add_reaction("💥")
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"There is no prompt like that -> {ctx.message.content}",
                            delete_after=3.5, mention_author=True)
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply("You have no permission to use this command !!!!",
                            delete_after=3.5, mention_author=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("It looks like you forgot somethings... You can use !help...",
                            delete_after=3.5, mention_author=True)
        else:
            await ctx.reply("An unknown error occured. Sorry...", delete_after=3.5, mention_author=True)


async def setup(bot):
    await bot.add_cog(UlakEvents(bot))
