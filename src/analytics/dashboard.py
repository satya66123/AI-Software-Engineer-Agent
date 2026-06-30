import os

def get_dashboard_stats(files):

    total_files = len(files)

    total_lines = 0

    extensions = {}

    print("=" * 50)

    for file in files:

        try:

            file_path = file["path"]

            print(f"Checking: {file_path}")

            print(
                f"Exists: {os.path.exists(file_path)}"
            )

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                lines = len(
                    f.readlines()
                )

                print(
                    f"Lines: {lines}"
                )

                total_lines += lines

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

        ext = file.get(
            "extension",
            "Unknown"
        )

        extensions[ext] = (
            extensions.get(ext, 0) + 1
        )

    print(
        f"TOTAL LINES = {total_lines}"
    )

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "extensions": extensions
    }