from discord import app_commands
from discord.ext import commands
import discord


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Shows how to use commands")
    async def help(self, interaction: discord.Interaction):
        message = """Welcome to slash command helper !
        - admin commands
            / You can adjust the accesible roles, Ulak's target channels and admin channels

            + admin set-role <role> <remove:False>
                / ...
            + admin unset-role <role>
                / ...
            + admin set-channel <channel> <remove:False>
                / ...
            + admin unset-channel <channel>
                / ...
            + admin test
                / You can use this command for test.
        
        - message commands

            / You can show or create messages with Ulak.
    
            + create <message>

                / When you run this command, Ulak send it to target channels that adjusted

            + show (In development)"""

        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
