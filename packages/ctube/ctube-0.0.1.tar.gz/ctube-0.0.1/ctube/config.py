import os
import toml
from ctube.paths import (
    CONFIG, 
    MUSIC,
    USER_CONFIG_DIR, 
    CLITUBE_CONFIG_DIR
)

os.makedirs(USER_CONFIG_DIR, exist_ok=True)
os.makedirs(CLITUBE_CONFIG_DIR, exist_ok=True)


DEFAULT_CONFIG = {
    "output_path": MUSIC,
    "skip_existing": True,
    "prompt_char": ">"
}


if os.path.exists(CONFIG):
    with open(CONFIG, "r") as f:
        config = toml.load(f)
else:
    with open(CONFIG, "w") as f:
        toml.dump(DEFAULT_CONFIG, f)
    config = DEFAULT_CONFIG
