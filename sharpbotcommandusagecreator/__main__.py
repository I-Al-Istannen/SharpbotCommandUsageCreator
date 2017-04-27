import argparse
import sys

import os

from sharpbotcommandusagecreator import githubparser
from sharpbotcommandusagecreator.descriptionextractor import get_description
from sharpbotcommandusagecreator.outputformatter import Formatter

user = "Rayzr522"
repo = "sharpbot"
sha = "master"
api_repo_url = "https://api.github.com/repos/%s/%s/git/trees/%s?recursive=1" \
               % (user, repo, sha)
commands_path = "src/commands"


def _build_download_url(path):
    return "https://raw.githubusercontent.com/Rayzr522/SharpBot/master/%s" \
           % path


def _filter_other_files(files):
    return [x for x in files
            if x["type"] == "blob"
            if x["path"].endswith("js")
            if x["path"].startswith(commands_path)
            if not x["path"].split("/")[-1].startswith("_")]


def _resolve_file(argument):
    if os.path.isfile(argument):
        with open(argument) as file:
            return file.read()
    raise FileNotFoundError(
          "Couldn't find file '%s' or is a directory!" % argument)


def _resolve_value(string):
    if string.startswith("/"):
        return _resolve_file(string[1:])
    return string.encode().decode("unicode_escape")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(*["-command_format", "-f"], nargs="?",
                        default=Formatter.default_format,
                        help="The format for the commands."
                             " Accepts a link to a file."
                             "\nAlso valid is 'no_category'.")
    parser.add_argument(*["-category-header", "-c"], nargs="?",
                        default="", help="The format for the category headers."
                                         " Accepts a link to a file.")

    parsed = parser.parse_args(sys.argv[1:])

    command_format = _resolve_value(parsed.command_format)
    if command_format == "no_category":
        command_format = Formatter.default_format_no_category
    category_header = _resolve_value(parsed.category_header)

    commands = _filter_other_files(githubparser.parse_github_tree(api_repo_url))
    command_descriptions = [
        get_description(_build_download_url(x["path"]),
                        x["path"].split("/")[-2])
        for x in commands
    ]

    formatter = Formatter(
          command_format=command_format,
          category_headings=category_header)
    formatter.format_commands(command_descriptions)
