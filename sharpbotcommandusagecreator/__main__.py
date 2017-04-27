import getopt
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


def _usage():
    print("Usage:")
    _print_arg_help("f", "format",
                    "The format for the commands. Accepts a link to a file."
                    "\nAlso valid are 'default' and 'no_category'.")
    _print_arg_help("c", "category-header",
                    "The format for the category headers."
                    " Accepts a link to a file.")
    _print_arg_help("h", "help",
                    "Shows this help")
    print("Both options can point to a file, following the format '/<path>'")


def _print_arg_help(short, long, description):
    print("-%s (--%s)" % (short, long))
    print("    %s" % description)


def _get_value(list_of_tuples, key):
    return [x[1] for x in list_of_tuples if x[0] == key]


def _resolve_file(argument):
    if os.path.isfile(argument):
        with open(argument) as file:
            return file.read()
    raise FileNotFoundError(
          "Couldn't find file '%s' or is a directory!" % argument)


if __name__ == '__main__':

    # Default formats
    command_format = Formatter.default_format
    category_header = ""

    try:
        opt, args = getopt.getopt(sys.argv[1:], shortopts="f:c:o:",
                                  longopts=["format=", "category-header="])
        opt_names = [x[0] for x in opt]

        if "-h" in opt_names or "--help" in opt_names:
            _usage()
            exit(2)

        if "-c" in opt_names or "--category-header" in opt_names:
            command_format = Formatter.default_format_no_category
            category_header = _get_value(opt, "--category-header")

            if category_header.__len__() == 0:
                category_header = _get_value(opt, "-c")

            category_header = "".join(category_header)

        if "-f" in opt_names or "--format" in opt_names:
            command_format = _get_value(opt, "--format")
            if command_format.__len__() == 0:
                command_format = _get_value(opt, "-f")

            command_format = "".join(command_format)

            if command_format == "default":
                command_format = Formatter.default_format
            elif command_format == "no_category":
                command_format = Formatter.default_format_no_category

        if command_format.startswith("/"):
            command_format = _resolve_file(command_format[1:])
        if category_header.startswith("/"):
            category_header = _resolve_file(category_header[1:])

        # Allow the use of "\n" and stuff
        category_header = category_header.encode().decode("unicode_escape")
        command_format = command_format.encode().decode("unicode_escape")
    except getopt.GetoptError:
        _usage()
        exit(2)

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
