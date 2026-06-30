import re

def validate_github_url(url):
    pattern = r"^https://github\.com/([^/]+)/([^/]+)/?$"

    match = re.match(pattern, url)

    if match:
        owner = match.group(1)
        repo = match.group(2)

        return {
            "valid": True,
            "owner": owner,
            "repo": repo
        }

    return {
        "valid": False
    }