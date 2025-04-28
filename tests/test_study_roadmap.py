import os
import json
import tempfile
import pytest
from study_roadmap import StudyRoadmap


@pytest.fixture
def temp_roadmap_file():
    # Archivo temporal con skills vacías
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8")
    json.dump({"skills": []}, temp_file)
    temp_file.close()
    yield temp_file.name
    os.remove(temp_file.name)


def test_add_skill(temp_roadmap_file, capsys):
    roadmap = StudyRoadmap(temp_roadmap_file)
    roadmap.add_skill("Python", "urgente")
    assert any(
        s["name"] == "Python" and s["priority"] == "urgente" for s in roadmap.skills
    )


def test_add_skill_invalid_priority(temp_roadmap_file, capsys):
    roadmap = StudyRoadmap(temp_roadmap_file)
    roadmap.add_skill("CSS", "media")
    captured = capsys.readouterr()
    assert "❌ Prioridad inválida" in captured.out


def test_update_priority(temp_roadmap_file):
    roadmap = StudyRoadmap(temp_roadmap_file)
    roadmap.add_skill("Flask", "clave")
    roadmap.update_priority("Flask", "urgente")
    assert any(
        s["name"] == "Flask" and s["priority"] == "urgente" for s in roadmap.skills
    )


def test_update_priority_invalid(temp_roadmap_file, capsys):
    roadmap = StudyRoadmap(temp_roadmap_file)
    roadmap.add_skill("Django", "clave")
    roadmap.update_priority("Django", "alta")
    captured = capsys.readouterr()
    assert "❌ Prioridad inválida" in captured.out


def test_export_skills_md(temp_roadmap_file):
    roadmap = StudyRoadmap(temp_roadmap_file)
    roadmap.add_skill("FastAPI", "interesante")
    export_path = tempfile.NamedTemporaryFile(delete=False).name
    roadmap.export_skills(format="md", output_path=export_path)

    with open(export_path, encoding="utf-8") as f:
        content = f.read()
    assert "**FastAPI**" in content
    os.remove(export_path)


def test_export_skills_html(temp_roadmap_file):
    roadmap = StudyRoadmap(temp_roadmap_file)
    roadmap.add_skill("SQLite", "clave")
    export_path = tempfile.NamedTemporaryFile(delete=False).name
    roadmap.export_skills(format="html", output_path=export_path)

    with open(export_path, encoding="utf-8") as f:
        content = f.read()
    assert "<strong>SQLite</strong>" in content
    os.remove(export_path)
