from discord.ext import commands
import discord
import utils
import checks


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create")
    @commands.check(checks.text_command_has_permission)
    async def create(self, ctx: commands.Context, *, message):
        """
        Sends the message parameter to the all target-channels
        :param message: The message to send
        """
        target_channel_ids = utils.get_guild_info(ctx.guild.id)['target-channel-ids']
        target_channels = [discord.utils.get(ctx.guild.text_channels, id=int(_id)) for _id in target_channel_ids]

        await ctx.message.add_reaction("🐺")

        for channel in target_channels:
            await channel.send("💌" + message)


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageCommands(bot))
