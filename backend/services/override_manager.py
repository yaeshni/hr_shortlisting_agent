import json
import os

# FIX: Use a path relative to this file so it always saves in the same place
# regardless of where you run uvicorn from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OVERRIDE_FILE = os.path.join(BASE_DIR, "..", "overrides.json")


def save_override(data):
    overrides = []

    if os.path.exists(OVERRIDE_FILE):
        with open(OVERRIDE_FILE, "r") as f:
            try:
                overrides = json.load(f)
            except json.JSONDecodeError:
                overrides = []

    overrides.append(data)

    with open(OVERRIDE_FILE, "w") as f:
        json.dump(overrides, f, indent=4)


def load_overrides():
    if not os.path.exists(OVERRIDE_FILE):
        return []
    with open(OVERRIDE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []