from typing import Literal, Union
from discord.ext import commands
import discord
import utils
import checks


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keys = {
            'role': 'accessible-roles',
            'target_channel': 'target-channel-ids',
            'admin_channel': 'admin-channel-ids'
        }

    @checks.has_permission()
    @commands.command(name="set")
    async def add(
            self,
            ctx: commands.Context,
            _type: Literal['role', 'target_channel', 'admin_channel'],
            _object: Union[discord.Role, discord.TextChannel],
            remove=False
    ):
        """
        Sets the accessible roles, target channels and admin channels.
        :param _type: ['role', 'target_channel', 'admin_channel']
        :param _object: Role or channel...
        """

        key = self.keys[_type]

        guild_data = utils.get_guild_info(ctx.guild.id)
        objects = guild_data[key].copy()

        if remove and str(_object.id) in objects:
            objects.remove(str(_object.id))
        else:
            objects.append(str(_object.id))

        guild_data[key] = list(set(objects))
        utils.update_guild({str(ctx.guild.id): guild_data})

        if remove:
            await ctx.send(f"{_object.name} removed from {_type} list")
        else:
            await ctx.send(f"{_object.name} setted as {_type}")

    @checks.has_permission()
    @commands.command(name="unset")
    async def delete(
            self,
            ctx: commands.Context,
            _type: Literal['role', 'target_channel', 'admin_channel'],
            _object: Union[discord.Role, discord.TextChannel, None]
    ):

        """
        Unsets the accessible roles, target channels and admin channels.
        :param _type: ['role', 'target_channel', 'admin_channel']
        :param _object: Role or channel...
        """
        await self.add(ctx, _type, _object, remove=True)

    @checks.has_permission()
    @commands.command(name="show")
    async def show(
            self,
            ctx: commands.Context,
            _type: Literal['role', 'target_channel', 'admin_channel', 'all']
    ):
        """
        Shows the accessible roles, target channels and admin channels.
        :param _type: ['role', 'target_channel', 'admin_channel']
        """

        if _type == 'all':
            modes = ['role', 'target_channel', 'admin_channel']
            for mode in modes:
                await self.show(ctx, mode)
        else:
            data = utils.get_guild_info(ctx.guild.id)
            message = f"{_type.title()} List:\n"
            key = self.keys[_type]
            id_list = data.get(key)
            iterable = ctx.guild.text_channels if _type != 'role' else ctx.guild.roles

            for _id in id_list:
                dc_obj = discord.utils.get(iterable, id=int(_id))
                message += dc_obj.name + "\n"

            await ctx.send(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            utils.funny_log(f"{ctx.author.display_name} tried to run addrole function...")

        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            utils.funny_log(str(error))


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))
