from discord.ext import commands
from events import UlakEvents
from text_commands.help import HelpCommand
import discord.errors
import settings
import utils


logger = settings.logging.getLogger("bot")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=HelpCommand())


@bot.event
async def on_ready():
    await bot.load_extension("events")
    await bot.load_extension("text_commands.admin_commands")
    await bot.load_extension("text_commands.message_commands")
    await bot.load_extension("slash_commands.admin_commands")
    await bot.load_extension("slash_commands.message_commands")
    await bot.load_extension("slash_commands.help")

    saved_guild_ids = list(utils.get_all_guilds().keys())
    whole_guild_ids = [str(guild.id) for guild in bot.guilds]
    different_ids = list(set(whole_guild_ids).difference(saved_guild_ids))

    for guild in bot.guilds:
        if str(guild.id) in different_ids:
            await UlakEvents.p_on_guild_join(guild)


if __name__ == '__main__':
    bot.run(token=settings.DISCORD_BOT_TOKEN, root_logger=True)
