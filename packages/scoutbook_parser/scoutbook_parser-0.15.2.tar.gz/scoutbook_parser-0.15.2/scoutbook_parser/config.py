import os
from pathlib import Path

import toml

basedir = Path(os.path.dirname(__file__))

CONFIG = toml.load(basedir / "config.toml")
