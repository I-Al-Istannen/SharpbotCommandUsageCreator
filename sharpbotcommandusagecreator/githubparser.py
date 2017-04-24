import json

from sharpbotcommandusagecreator.webutil import get_web_page


def parse_github_tree(github_tree_url):
    """"Parses a github tree url to response json objects.
    
    The resulting dict has at least the following keys:
       "path" ==> The path to the file\n
       "type" ==> "tree" for a directory, "blob" for a file. Maybe more.\n
       "sha"  ==> The sha hash of the\n 
    :param github_tree_url: The github url to parse
    :return: A list with the returned Json elements.
    """
    html = get_web_page(github_tree_url)
    loaded_json = json.loads(html)
    all_files = []
    for entry in loaded_json["tree"]:
        all_files.append(entry)

    return all_files
