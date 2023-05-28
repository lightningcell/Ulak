from discord import app_commands
from typing import Literal, Union
import checks
import discord
import utils


class Admin(app_commands.Group):
    keys = {
        'Role': 'accessible-roles',
        'Target Channel': 'target-channel-ids',
        'Admin Channel': 'admin-channel-ids'
    }

    async def adjust(self, interaction, _type, _object, remove):
        key = self.keys[_type]
        guild_data = utils.get_guild_info(interaction.guild_id)
        objects = guild_data[key].copy()

        if remove and str(_object.id) in objects:
            objects.remove(str(_object.id))
        else:
            objects.append(str(_object.id))

        guild_data[key] = list(set(objects))
        utils.update_guild({str(interaction.guild_id): guild_data})
        name, _list = (_object.name, "accessible roles")  if _type == "Role" else (_object.mention, _type.lower())

        if remove:
            await interaction.response.send_message(f"{name} removed from {_list} list", ephemeral=True)
        else:
            await interaction.response.send_message(f"{name} setted as {_list}", ephemeral=True)

    def __show(self, interaction, _type):
        data = utils.get_guild_info(interaction.guild_id)
        message = f"{_type.title()} List:\n"
        key = self.keys[_type.title()]
        id_list = data.get(key)
        iterable = interaction.guild.text_channels if _type != 'Role' else interaction.guild.roles

        for _id in id_list:
            dc_obj = discord.utils.get(iterable, id=int(_id))
            message += (dc_obj.name if _type == 'Role' else dc_obj.mention) + "\n"

        return message

    @app_commands.command(name="set-role", description="Adjust the accessible roles")
    @app_commands.describe(
        role="Choose the role to be added.",
        remove="Set true, if you want to remove that role or just use unset-role command (recommended)"
    )
    @app_commands.check(checks.app_command_has_permission)
    async def set_role(self, interaction: discord.Interaction, role: discord.Role, remove: bool = False):
        await self.adjust(interaction, "Role", role, remove)

    @app_commands.command(name="set-channel", description="Adjust the target channels and admin channels")
    @app_commands.describe(
        channel="Choose the channel to be added.",
        _type="Choose the channel type",
        remove="Set true, if you want to remove that channel or just use unset-channel command (recommended)"
    )
    @app_commands.rename(_type="type")
    @app_commands.check(checks.app_command_has_permission)
    async def set_channel(
            self,
            interaction: discord.Interaction,
            _type: Literal['Target Channel', 'Admin Channel'],
            channel: discord.TextChannel,
            remove: bool = False
    ):
        await self.adjust(interaction, _type, channel, remove)

    @app_commands.command(name="unset-role", description="Adjust the accessible roles")
    @app_commands.describe(
        role="Choose the role to be removed"
    )
    @app_commands.check(checks.app_command_has_permission)
    async def unset_role(self, interaction: discord.Interaction, role: discord.Role):
        await self.adjust(interaction, "Role", role, remove=True)

    @app_commands.command(name="unset-channel", description="Adjust the target channels and admin channels")
    @app_commands.describe(
        channel="Choose the channel to be removed",
        _type="Choose the channel type",
    )
    @app_commands.rename(_type="type")
    @app_commands.check(checks.app_command_has_permission)
    async def unset_channel(
            self,
            interaction: discord.Interaction,
            _type: Literal['Target Channel', 'Admin Channel'],
            channel: discord.TextChannel
    ):
        await self.adjust(interaction, _type, channel, remove=True)

    @app_commands.command(name="show", description="Show the target channels, admin channels and accessible roles.")
    @app_commands.describe(
        _type="Choose what do you want to see.",
    )
    @app_commands.rename(_type="type")
    @app_commands.check(checks.app_command_has_permission)
    async def show(self, interaction: discord.Interaction, _type: Literal['All', 'Role', 'Admin Channel', 'Target Channel']):
        message = ""
        if _type == 'All':
            modes = ['Role', 'Target Channel', 'Admin Channel']
            for mode in modes:
                message += self.__show(interaction, mode)
        else:
            message = self.__show(interaction, _type)

        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="test")
    @app_commands.check(checks.app_command_has_permission)
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("This is a test.", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError, /) -> None:
        print(error)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You have no permission to use this command !", ephemeral=True)
        else:
            await interaction.response.send_message("An unknown error occured !")


async def setup(bot):
    bot.tree.add_command(Admin(name="admin", description="Admin commands for adjust bot settings"))
