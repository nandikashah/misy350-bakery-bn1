import json
from pathlib import Path
from typing import List, Dict


class BakeryStore:
    def __init__(self, json_path: Path) -> None:
        self.json_path = json_path

    def load(self) -> List[Dict]:
        if self.json_path.exists():
            with open(self.json_path, "r") as f:
                return json.load(f)
        return []

    def save(self, data: List[Dict]) -> None:
        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=4)