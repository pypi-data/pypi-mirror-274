import re

URL_REG = re.compile("(http://|https://)?([^:/]*)(?::(\d+))?(/.*)?")


def clean_url_host(url):
    """
    Clean the url:
    * Add scheme if missing
    * Remove trailing slash and path
    * Extract the host
    """
    scheme, host, port, _ = URL_REG.match(url).groups()
    scheme = scheme or "https://"
    url = scheme + host + (f":{port}" if port else "")
    return url, host, port
