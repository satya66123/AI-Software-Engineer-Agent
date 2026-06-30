import json
import os

SETTINGS_FILE = "settings.json"


def load_settings():

    if os.path.exists(
        SETTINGS_FILE
    ):

        with open(
            SETTINGS_FILE,
            "r"
        ) as f:

            return json.load(f)

    return {

        "theme": "Light",

        "default_model":
            "qwen2.5:1.5b",

        "top_k": 5
    }


def save_settings(
    settings
):

    with open(
        SETTINGS_FILE,
        "w"
    ) as f:

        json.dump(
            settings,
            f,
            indent=4
        )