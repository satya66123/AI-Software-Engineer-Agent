from git import Repo
import os
from datetime import datetime


def clone_repository(repo_url):

    repo_name = repo_url.rstrip("/").split("/")[-1]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    clone_path = os.path.join(
        "cloned_repos",
        f"{repo_name}_{timestamp}"
    )

    Repo.clone_from(
        repo_url,
        clone_path
    )

    return clone_path