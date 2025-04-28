import json
from typing import List

VALID_PRIORITIES = {"urgente", "clave", "interesante"}
PRIORITY_ORDER = {"urgente": 0, "clave": 1, "interesante": 2, "desconocida": 99}


class StudyRoadmap:
    def __init__(self, roadmap_path: str):
        self.path = roadmap_path
        self.skills = self._load_skills()

    def _load_skills(self) -> List[str]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("skills", [])

    def add_skill(self, name: str, priority: str) -> None:
        if priority not in VALID_PRIORITIES:
            print(
                f"❌ Prioridad inválida: '{priority}' (usa: urgente, clave, interesante)"
            )
            return
        if any(s["name"] == name for s in self.skills):
            print(f"⚠️ Ya existe una skill con el nombre '{name}'")
            return
        self.skills.append({"name": name, "priority": priority})
        self.save()

    def update_priority(self, name: str, new_priority: str) -> None:
        if new_priority not in VALID_PRIORITIES:
            print(
                f"❌ Prioridad inválida: '{new_priority}' (usa: urgente, clave, interesante)"
            )
            return
        for skill in self.skills:
            if skill["name"] == name:
                skill["priority"] = new_priority
                self.save()
                return
        print(f"❌ No se encontró la skill '{name}'")

    def get_skills_by_priority(self, priority: str) -> List[str]:
        return [
            skill["name"] for skill in self.skills if skill.get("priority") == priority
        ]

    def list_skills(self) -> None:
        sorted_skills = sorted(
            self.skills, key=lambda s: PRIORITY_ORDER.get(s["priority"], 99)
        )
        skills = []
        for skill in sorted_skills:
            print(f"{skill['name']} → {skill['priority']}")
            skills.append(skill["name"])
        return skills

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"skills": self.skills}, f, indent=2, ensure_ascii=False)

    def export_skills(
        self, format: str = "md", output_path: str = "skills_export.md"
    ) -> None:
        sorted_skills = sorted(
            self.skills, key=lambda s: PRIORITY_ORDER.get(s["priority"], 99)
        )

        if format == "md":
            content = "# Lista de Skills por Prioridad\n\n"
            for skill in sorted_skills:
                content += f"- **{skill['name']}** → `{skill['priority']}`\n"
        elif format == "html":
            content = "<h1>Lista de Skills por Prioridad</h1>\n<ul>\n"
            for skill in sorted_skills:
                content += f"<li><strong>{skill['name']}</strong> → <code>{skill['priority']}</code></li>\n"
            content += "</ul>"
        else:
            raise ValueError("Formato no soportado. Usá 'md' o 'html'.")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✔ Exportado exitosamente como {output_path}")
