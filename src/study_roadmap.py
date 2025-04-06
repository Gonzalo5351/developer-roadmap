import json
from typing import List

class StudyRoadmap:
    def __init__(self, roadmap_path: str):
        self.skills = self._load_skills(roadmap_path)

    def _load_skills(self, path: str) -> List[str]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("skills", [])
