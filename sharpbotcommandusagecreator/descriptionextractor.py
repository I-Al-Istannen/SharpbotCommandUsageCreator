import demjson

from sharpbotcommandusagecreator.webutil import get_web_page


def get_description(github_raw_url, parent_folder):
    """Returns the description for a command, given the raw github url.
    
    :param github_raw_url: The raw.github.com url to the file
    :param parent_folder: The parent folder of the file. Used as category
    """
    description_json = _extract_description_part(
          get_web_page(github_raw_url).decode().splitlines()
    )
    description_dict = demjson.decode(description_json)
    description_dict["parent_folder"] = parent_folder
    return description_dict


def _extract_description_part(lines):
    description = ""
    in_info_bracket = False
    for (index, string) in enumerate(lines):
        if string.startswith("exports.info"):
            in_info_bracket = True

        if in_info_bracket and string.startswith("}"):
            in_info_bracket = False

        if in_info_bracket:
            description += string + "\n"

    description = description.replace("exports.info = ", "")
    return description + "}"
