from discord.ext import commands
import discord


class HelpCommand(commands.HelpCommand):
    set_command_head = """- !set command

        / You can adjust the accesible roles, Ulak's target channels and admin channels

        Usage: !set <type> <object> <remove: False>"""

    set_command_body = """   Explanation
            + type -> You can choose role, target_channel, admin_channel
            + object -> You can text a role or channel name
            + remove -> It is False by default. You can set True if you want to remove the object from type list.
            + NOTE: You don't have to use the remove, you can use unset command."""

    unset_command_head = """- !unset command

        / You can adjust the accesible roles, Ulak's target channels and admin channels

        Usage: !set <type> <object>"""

    unset_command_body = """    Explanation
            + type -> You can choose role, target_channel, admin_channel
            + object -> You can text a role or channel name"""

    show_command_head = """- !show command

        / You can show the accesible roles, Ulak's target channels and admin channels

        Usage: !show <type>"""

    show_command_body = """    Explanation
            + type -> You had to choose one of them; role, target_channel, admin_channel, all"""

    create_command_head = """- !create command
        / You can create messages to send target channels with Ulak.

        Usage: !create <message>"""

    create_command_body = """    Explanation
            + message -> The message that you will send to target channels."""

    message = f"""Welcome to text command helper !
    {set_command_head}

    {set_command_body}

    {unset_command_head}

    {unset_command_body}

    {show_command_head}

    {show_command_body}

    {create_command_head}

    {create_command_body}"""

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        await channel.send(self.message)

    async def send_command_help(self, command):
        message = {
            "set": self.set_command_head + "\n" + self.set_command_body,
            "unset": self.unset_command_head + "\n" + self.unset_command_body,
            "show": self.show_command_head + "\n" + self.show_command_body,
            "create": self.create_command_head + "\n" + self.create_command_body
        }.get(str(command))

        channel = self.get_destination()

        if command:
            await channel.send(message)
        else:
            await channel.send("⁉⁉⁉⁉⁉")
