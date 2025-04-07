import json
from typing import List

class StudyRoadmap:
    def __init__(self, roadmap_path: str):
        self.path = roadmap_path
        self.skills = self._load_skills()

    def _load_skills(self) -> List[str]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("skills", [])
