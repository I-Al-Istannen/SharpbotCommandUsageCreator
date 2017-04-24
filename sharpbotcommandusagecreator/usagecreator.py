import sharpbotcommandusagecreator.githubparser as parser
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


if __name__ == '__main__':
    commands = _filter_other_files(parser.parse_github_tree(api_repo_url))
    command_descriptions = [
        get_description(_build_download_url(x["path"]),
                        x["path"].split("/")[-2])
        for x in commands
    ]

    Formatter.create_default().format_commands(command_descriptions)
