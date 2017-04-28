import re


class Formatter(object):
    default_format = """### `{name}`
*Description:* `{description}`
*Usage:* `{usage}`
<if>*Credits:* `{credits}`
*Category:* `{category}`"""

    default_format_no_category = """### `{name}`
*Description:* `{description}`
*Usage:* `{usage}`
<if>*Credits:* `{credits}`"""

    def __init__(self, command_format=default_format, category_headings=""):
        """Creates a new Formatter.

        The replaced keys for the format are: \n
        `name` ==> The name \n
        `description` ==> The description \n
        `usage` ==> The usage \n
        `credits` ==> The credits \n
        `category` ==> The category \n

        :param command_format: The format of the command.
        :param category_headings: The format for category headings.
        """
        self._command_format = command_format
        self.category_headings = category_headings

    def format_commands(self, command_descriptions):
        for command in command_descriptions:
            print(self._format_command(command))
            print()

    def _format_command(self, command):
        name = _get_or_default(command, "name", "N/A")
        description = _get_or_default(command, "description", "N/A")
        usage = _get_or_default(command, "usage", "N/A")
        command_credits = _get_or_default(command, "credits", "N/A")
        category = _get_or_default(command, "parent_folder", "N/A")

        if self.category_headings:
            if not hasattr(self, "last_category") \
                  or category != self.last_category:
                self.last_category = category
                print(
                      self.category_headings.format(category=category)
                )

        new_format = []
        for line in self._command_format.splitlines():
            if line.startswith("<if>"):
                if _should_remove(line, command):
                    continue
                line = line["<if>".__len__():]
            new_format.append(line)

        new_format = "  \n".join(new_format)
        return new_format.format(name=name,
                                 description=description,
                                 usage=usage,
                                 credits=command_credits,
                                 category=category)


def _should_remove(line, command):
    pattern = re.compile("{(.+)\\}")
    for match in pattern.findall(line):
        if match not in command:
            return True
    return False


def _get_or_default(command, key, default):
    return command[key] if key in command else default
