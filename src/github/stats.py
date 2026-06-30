import os

def calculate_stats(files):

    total_lines = 0

    for file in files:

        try:

            with open(
                file["path"],
                "r",
                encoding="utf-8"
            ) as f:

                total_lines += len(
                    f.readlines()
                )

        except:
            pass

    return {
        "total_files": len(files),
        "total_lines": total_lines
    }