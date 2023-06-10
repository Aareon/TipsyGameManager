from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Game:
    folder: Path
    name: str
    version: str
    description: str
    binaries: List
