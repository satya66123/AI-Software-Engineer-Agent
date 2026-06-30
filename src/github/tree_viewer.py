import os

IGNORE_FOLDERS = {
    ".git",
    "__pycache__",
    "venv",
    "node_modules",
    ".idea",
    ".vscode"
}

def generate_tree(path):

    tree = []

    for root, dirs, files in os.walk(path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_FOLDERS
        ]

        level = root.replace(
            path,
            ""
        ).count(os.sep)

        indent = "    " * level

        tree.append(
            f"{indent}{os.path.basename(root)}/"
        )

        sub_indent = "    " * (level + 1)

        for file in sorted(files):

            tree.append(
                f"{sub_indent}{file}"
            )

    return tree