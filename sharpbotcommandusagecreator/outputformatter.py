import re


class Formatter(object):
    def __init__(self, command_format):
        self._command_format = command_format

    @classmethod
    def create_default(cls):
        return Formatter("""### `{name}`  
*Description:* `{description}`  
*Usage:* `{usage}`  
<if>*Credits:* `{credits}`  
*Category:* `{parent_folder}`  """)

    def format_commands(self, command_descriptions):
        for command in command_descriptions:
            print(self._format_command(command))
            print()

    def _format_command(self, command):
        name = _get_or_default(command, "name", "N/A")
        description = _get_or_default(command, "description", "N/A")
        usage = _get_or_default(command, "usage", "N/A")
        command_credits = _get_or_default(command, "credits", "N/A")
        parent_folder = _get_or_default(command, "parent_folder", "N/A")

        new_format = []
        for line in self._command_format.splitlines():
            if line.startswith("<if>"):
                if _should_remove(line, command):
                    continue
                line = line["<if>".__len__():-1]
            new_format.append(line)

        new_format = "\n".join(new_format)
        return new_format.format(name=name,
                                 description=description,
                                 usage=usage,
                                 credits=command_credits,
                                 parent_folder=parent_folder)


def _should_remove(line, command):
    pattern = re.compile("{(.+)\\}")
    for match in pattern.findall(line):
        if match not in command:
            return True
    return False


def _get_or_default(command, key, default):
    return command[key] if key in command else default
