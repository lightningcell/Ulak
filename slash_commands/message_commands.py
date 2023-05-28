from discord import app_commands
from typing import Literal, Union
import checks
import discord
import utils


class MessageCommands(app_commands.Group):
    @app_commands.command(name="create", description="Message commands...")
    @app_commands.describe(
        message="The message that you will give to the Ulak"
    )
    @app_commands.check(checks.app_command_has_permission)
    async def create(self, interaction: discord.Interaction, message: str):
        target_channel_ids = utils.get_guild_info(interaction.guild_id)['target-channel-ids']
        target_channels = [discord.utils.get(interaction.guild.text_channels, id=int(_id)) for _id in target_channel_ids]

        if target_channel_ids:
            await interaction.response.send_message("The message is in Ulak...", ephemeral=True)

        for channel in target_channels:
            await channel.send("💌" + message)

    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError, /) -> None:
        print(error)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You have no permission to use this command !", ephemeral=True)
        else:
            await interaction.response.send_message("An unknown error occured !")


async def setup(bot):
    bot.tree.add_command(MessageCommands(name="message", description="Message commands for Ulak"))
