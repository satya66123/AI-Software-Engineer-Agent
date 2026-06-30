import os

def read_readme(repo_path):

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.lower() == "readme.md":

                readme_path = os.path.join(
                    root,
                    file
                )

                try:

                    with open(
                        readme_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        return f.read()

                except Exception:

                    return None

    return None