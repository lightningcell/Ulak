from datetime import datetime
import json
import settings
from typing import Literal


def _get_by_file(file_name: str) -> dict:
    """
    :param file_name: .json file name in the data folder
    :return: Returns file content as dict
    """
    json_files = [file.name for file in settings.DATA_DIR.glob("*.json")]
    if file_name not in json_files:
        return {}
    else:
        with open(settings.DATA_DIR / file_name, "r") as file:
            file.seek(0)
            content = json.load(file)
            return content


def get_base_data(local_code) -> dict:
    """
    :param local_code: discord.Guild.preferred_locale
    :return: Returns the local content of base.json file as dict
    """
    base_json = _get_by_file("base.json")
    result = base_json.get(str(local_code))

    return result if result else base_json["en-US"]


def get_all_guilds() -> dict:
    """
    :return: Returns content of guild_info.json as dict
    """
    return _get_by_file("guild_info.json")


def get_scheme(scheme_name: Literal['error_scheme', 'guild_scheme']) -> dict:
    """
    :param scheme_name: Specified parameter -> ['error_scheme', 'guild_scheme']
    :return: Returns the scheme in the schemes.json as dict
    """
    schemes = _get_by_file("schemes.json")
    return schemes[scheme_name] if scheme_name in schemes else schemes["error_scheme"]


def get_guild_info(guild_id: int) -> dict:
    """
    :param guild_id: discord.Guild.id
    :return: Returns guild data in the guild_info.json as dict by id.
    """
    guilds = get_all_guilds()
    return guilds[str(guild_id)] if str(guild_id) in guilds else {}


def update_guild(guild_dict: dict, remove: bool = False) -> dict:
    """
    :param guild_dict:  The data that shaped by structure {<guild_id>: <guild_scheme>}
    :param remove: If remove is equals to True, removes the guild data from guild_info.json
    :return: Returns updated guilds.json as dict
    """
    guild_id = str(list(guild_dict.keys())[0])
    guilds = get_all_guilds()

    if remove and guild_id in guilds:
        guilds.pop(guild_id)
    else:
        guilds.update(guild_dict)

    with open(settings.DATA_DIR / "guild_info.json", "w") as file:
        file.seek(0)
        json.dump(guilds, file, indent=4, )

    return guilds


def add_guild(guild_id: int) -> dict:
    """
    Builds the guild structure and updates the guild_info.json
    :param guild_id: discord.Guild.id
    :return: Returns builded structure as dict
    """
    guild_dict = {str(guild_id): get_scheme("guild_scheme")}
    update_guild(guild_dict)
    return guild_dict


def remove_guild(guild_id: int) -> None:
    """
    :param guild_id: discord.Guild.id
    :return: None
    """
    update_guild({str(guild_id): {}}, remove=True)


def funny_log(line: str) -> None:
    """
    :param line: The data to be added to funny.log file
    :return: None
    """
    with open(settings.BASE_DIR / "logs" / "funny.log", "a") as file:
        file.write(line + str(datetime.now()) + "\n")
