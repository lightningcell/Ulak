from discord.ext import commands
from cogs.events import UlakEvents
import discord.errors
import settings
import utils


logger = settings.logging.getLogger("bot")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.load_extension("cogs.admin_commands")
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.message_commands")

    saved_guild_ids = list(utils.get_all_guilds().keys())
    whole_guild_ids = [str(guild.id) for guild in bot.guilds]
    different_ids = list(set(whole_guild_ids).difference(saved_guild_ids))

    for guild in bot.guilds:
        if guild.id in different_ids:
            await UlakEvents.p_on_guild_join(guild)


if __name__ == '__main__':
    bot.run(token=settings.DISCORD_BOT_TOKEN, root_logger=True)
