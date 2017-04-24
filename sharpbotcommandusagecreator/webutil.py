from urllib.request import urlopen


def get_web_page(url):
    """Returns the web page with the given url as a string
    
    :param url: The url to the page
    """
    with urlopen(url) as response:
        return response.read()
