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

    @commands.command(name="set")
    @commands.check(checks.text_command_has_permission)
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
        if (
                (not (_type == "role" and isinstance(_object, discord.Role)))
                and
                (not (_type in ("target_channel", "admin_channel") and isinstance(_object, discord.TextChannel)))
        ):
            await ctx.message.add_reaction("❌")
            await ctx.reply(f"You had to text a {_type}, if you choose type as {_type}. (Or just use slash commands :))")
        else:
            key = self.keys[_type]

            guild_data = utils.get_guild_info(ctx.guild.id)
            objects = guild_data[key].copy()

            if remove and str(_object.id) in objects:
                objects.remove(str(_object.id))
            else:
                objects.append(str(_object.id))

            guild_data[key] = list(set(objects))
            utils.update_guild({str(ctx.guild.id): guild_data})
            await ctx.message.add_reaction("✔")

            if remove:
                await ctx.reply(f"{_object.name} removed from {_type} list")
            else:
                await ctx.reply(
                    f"{_object.name} setted as {_type}"
                )

    @commands.command(name="unset")
    @commands.check(checks.text_command_has_permission)
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

    @commands.command(name="show")
    @commands.check(checks.text_command_has_permission)
    async def show(
            self,
            ctx: commands.Context,
            _type: Literal['role', 'target_channel', 'admin_channel', 'all']
    ):
        """
        Shows the accessible roles, target channels and admin channels.
        :param _type: ['role', 'target_channel', 'admin_channel']
        """

        await ctx.message.add_reaction("📨")

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
        await ctx.message.add_reaction("💥")
        if isinstance(error, discord.ext.commands.CheckFailure):
            utils.funny_log(f"{ctx.author.display_name} tried to run a command...")

        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            utils.funny_log(str(error))


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))
