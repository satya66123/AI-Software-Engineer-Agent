import os
from src.utils.logger import logger


SUPPORTED_EXTENSIONS = (
    ".py",
    ".java",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".sql",
    ".json",
    ".md"
)

IGNORE_FOLDERS = (
    ".git",
    "__pycache__",
    "venv",
    "node_modules"
)

def scan_repository(repo_path):

    files_data = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_FOLDERS
        ]

        for file in files:

            if file.endswith(
                SUPPORTED_EXTENSIONS
            ):

                full_path = os.path.join(
                    root,
                    file
                )

                files_data.append({
                    "name": file,
                    "path": full_path,
                    "extension": os.path.splitext(file)[1]
                })

                logger.info(f"Scanning repository: {full_path}")

                logger.info(f"Files found: {len(files_data)}")

    return files_data