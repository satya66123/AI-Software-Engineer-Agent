from collections import Counter

EXTENSION_MAP = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
    ".json": "JSON",
    ".md": "Markdown"
}

def detect_languages(files):

    language_count = Counter()

    for file in files:

        ext = file["extension"]

        language = EXTENSION_MAP.get(
            ext,
            "Other"
        )

        language_count[language] += 1

    return dict(language_count)