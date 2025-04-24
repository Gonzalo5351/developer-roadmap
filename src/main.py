import argparse
from study_roadmap import StudyRoadmap


def main():
    parser = argparse.ArgumentParser(description="🎓 Gestor de tu roadmap autodidacta")
    parser.add_argument(
        "command", choices=["add", "update", "list", "export"], help="Acción a realizar"
    )
    parser.add_argument("name", nargs="?", help="Nombre de la skill")
    parser.add_argument(
        "priority", nargs="?", help="Prioridad (urgente, clave, interesante)"
    )
    parser.add_argument(
        "--format", choices=["md", "html"], default="md", help="Formato de exportación"
    )
    parser.add_argument(
        "--output", default="skills_export.md", help="Ruta del archivo exportado"
    )

    args = parser.parse_args()
    roadmap = StudyRoadmap("roadmap.json")

    if args.command == "add":
        if args.name and args.priority:
            roadmap.add_skill(args.name, args.priority)
        else:
            print("❌ Para 'add' se requiere 'name' y 'priority'")
    elif args.command == "update":
        if args.name and args.priority:
            roadmap.update_priority(args.name, args.priority)
        else:
            print("❌ Para 'update' se requiere 'name' y 'new_priority'")
    elif args.command == "list":
        roadmap.list_skills()
    elif args.command == "export":
        roadmap.export_skills(format=args.format, output_path=args.output)


if __name__ == "__main__":
    main()
