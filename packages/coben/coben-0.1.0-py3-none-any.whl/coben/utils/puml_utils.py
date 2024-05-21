import os
import re
import logging
from utils.template_factory import TemplateFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UMLManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.template_factory = TemplateFactory(self.project_dir)  
        self.components_dir = os.path.join(project_dir, "components")
        self.project_name = os.path.basename(os.path.normpath(project_dir))
        self.uml_project_file = f"{self.project_name}.puml"
        self.uml_path = os.path.join(self.project_dir, self.uml_project_file)  

    def parse_hierarchy(self):
        hierarchy = {}
        stack = [hierarchy]  # Stack, der das aktuelle Level der Hierarchie hält

        try:
            with open(self.uml_path, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Fehler beim Lesen der Datei: {e}")
            return {}

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('@enduml'):
                continue
            
            if '{' in stripped_line:
                match = re.search(r'\b(component|rectangle)\s+"([^"]+)"\s*\{', stripped_line)
                if match:
                    element_type, element_name = match.groups()
                    current = {}
                    if element_name not in stack[-1]:  # Überprüfen, ob der Schlüssel schon existiert
                        stack[-1][element_name] = current
                    stack.append(current)  # Aktuelles Element zum Stack hinzufügen
            elif '}' in stripped_line:
                if len(stack) > 1:
                    stack.pop()  # Zurück zum übergeordneten Element

        print(f"Es gibt die Komponente: {hierarchy}")
        return hierarchy

    def format_puml_content(self, puml_content):
        lines = puml_content.splitlines()
        formatted_lines = []
        indent_level = 0
        indent_size = 4

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                continue

            if stripped_line.startswith('}'):
                indent_level -= 1

            formatted_line = ' ' * (indent_level * indent_size) + stripped_line
            formatted_lines.append(formatted_line)

            if '{' in stripped_line and not stripped_line.startswith('@enduml'):
                indent_level += 1

        return '\n'.join(formatted_lines)

    def generate_uml_from_structure(self, templates):
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
        for root, dirs, files in os.walk(self.components_dir):
            uml_components = [f"component {file[:-4]}" for file in files if file.endswith('.hpp')]
            if uml_components:
                component_name = os.path.basename(root)
                uml_code = templates['puml'].render(components=uml_components)
                md_file_path = os.path.join(self.docs_dir, f"{component_name}.md")
                self.append_uml_to_markdown(md_file_path, uml_code)

    def update_uml_file(self, hierarchy):
        lines = ['@startuml\n']
        def recurse_hierarchy(h, prefix=''):
            for name, sub_h in h.items():
                lines.append(f'component "{name}" {{\n')
                if sub_h:
                    recurse_hierarchy(sub_h, prefix + name + '/')
                lines.append('}\n')
        recurse_hierarchy(hierarchy)
        lines.append('@enduml\n```\n')
        with open(self.uml_path, 'w') as f:
            f.writelines(lines)

    def append_uml_to_markdown(self, md_file_path, uml_code):
        with open(md_file_path, 'a') as md_file:
            md_file.write(f"\n```puml\n{uml_code}\n```\n")

    def update_project_uml(self, project_name, modified_dirs):
        with open(self.uml_path, "r+") as file:
            content = file.read()
            for directory in modified_dirs:
                rectangle_definition = f"rectangle {directory} {{}}"
                if rectangle_definition not in content:
                    content += f"\n{rectangle_definition}"
            file.seek(0)
            file.write(content)
            file.truncate()
        print(f"Updated project UML for {project_name}")

    def create_project_uml(self):
        uml_content = self.template_factory.get_project_uml()

        with open(self.uml_path, 'w') as uml_file:
            uml_file.write(uml_content)
        logging.info("Zentrale UML-Datei erstellt.")

    def sync_project_diagram(self, project_name):
        modified_dirs = self.get_modified_directories()
        self.update_project_uml(project_name, modified_dirs)
        print(f"Synchronized project diagram for {project_name}")

    def sync_uml(self):
        uml_path = os.path.join(self.project_dir, self.uml_project_file)
        self.format_puml_content(uml_path)
        try:
            with open(uml_path, "r") as file:
                existing_lines = file.readlines()
        except FileNotFoundError:
            existing_lines = ["@startuml\n", "@enduml\n"]

        # Extrahieren der bereits definierten Komponenten
        existing_components = set()
        for line in existing_lines:
            if "component" in line and "{" in line:
                component_name = line.split("{")[0].split()[-1]
                existing_components.add(component_name)

        # Schreiben der aktualisierten UML-Datei
        with open(uml_path, "w") as file:
            file.write("@startuml\n")
            for component in os.listdir(self.components_dir):
                component_name = component[:-4]  # Entfernen von '.cpp'
                if component.endswith(".cpp") and component_name not in existing_components:
                    file.write(f"component {component_name} {{\n}}\n")

            # Die bestehenden Komponenten einfügen, die bereits in der UML-Datei waren
            for line in existing_lines:
                if "@startuml" not in line and "@enduml" not in line:
                    file.write(line)

            file.write("@enduml\n")
        logging.info("UML-Datei aktualisiert.")