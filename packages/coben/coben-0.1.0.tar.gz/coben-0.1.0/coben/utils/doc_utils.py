import os
import subprocess
import ruamel.yaml
from utils.template_factory import TemplateFactory  

yaml = ruamel.yaml.YAML()

class DocumentationManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.docs_dir = os.path.join(project_dir, "components")
        self.template_factory = TemplateFactory(self.docs_dir) 

    def create_component_markdown(self, component_name):
        md_content, cmake_content, hpp_content, cpp_content = self.template_factory.get_components_content(component_name)
        md_file_path = os.path.join(self.docs_dir, f"{component_name}.md")
        with open(md_file_path, "w") as file:
            file.write(md_content)
        self.update_mkdocs_config(component_name)            

    def setup_mkdocs_configuration(self):
        templatem = self.template_factory.get_mkdocs_config()
        mkdocs_path = os.path.join(self.project_dir, "mkdocs.yml")
        with open(mkdocs_path, "w") as file:
            file.write(templatem)

    def update_mkdocs_nav_recursively(self, hierarchy, nav_list):
        for component_name, sub_hierarchy in hierarchy.items():
            md_path = f"{component_name}/{component_name}.md"
            nav_entry = {component_name: md_path}
            if sub_hierarchy:  # Wenn es Unterkomponenten gibt, erstelle einen verschachtelten Eintrag
                sub_nav_list = []
                nav_entry = {component_name: sub_nav_list}
                self.update_mkdocs_nav_recursively(sub_hierarchy, sub_nav_list)
            nav_list.append(nav_entry)

    def update_navigation(self,hierarchy, base_path=""):
        nav = []
        for name, sub_hierarchy in hierarchy.items():
            component_md_path = f"{base_path}{name}/{name}.md"
            if sub_hierarchy:  # Hat Unterordner
                # Erstelle rekursiv Einträge für Unterordner
                sub_nav = self.update_navigation(sub_hierarchy, f"{base_path}{name}/")
                nav.append({name: [component_md_path] + sub_nav})
            else:
                # Erstelle einen Link zur Markdown-Datei dieser Komponente
                nav.append({name: component_md_path})
        return nav

    def update_mkdocs_nav(self, hierarchy):
        mkdocs_path = os.path.join(self.project_dir, "mkdocs.yml")
        with open(mkdocs_path, 'r') as file:
            mkdocs_config = yaml.load(file)

        # Aktualisiere die Navigation nur, wenn notwendig
        new_nav = self.update_navigation(hierarchy)
        if 'nav' not in mkdocs_config or mkdocs_config['nav'][0] != {'Components': new_nav}:
            mkdocs_config['nav'] = [{'Components': new_nav}]

            # Schreibe die aktualisierte Konfiguration zurück in die Datei
            with open(mkdocs_path, 'w') as file:
                yaml.dump(mkdocs_config, file)


    def create_new_component_from_markdown(self):
        for md_file in os.listdir(self.docs_dir):
            if md_file.endswith(".md"):
                # Lese die aktuelle UML-Datei und aktualisiere die Inhalte des Markdown
                #with open(os.path.join(project_dir, f"{project_dir}.puml"), "r") as uml_file:
                #    uml_content = uml_file.read()
                self.create_component_markdown(md_file)

    def create_index_md(self):
        template_factory = TemplateFactory(self.project_dir) # other directory
        index_content = template_factory.get_index_markdown()
        index_md_path = os.path.join(self.docs_dir, "index.md")
        with open(index_md_path, 'w') as index_file:
            index_file.write(index_content)

    def serve_mkdocs(self):
        mkdocs_config_path = os.path.join(self.project_dir, "mkdocs.yml")
        subprocess.run(["mkdocs", "serve", "--config-file", mkdocs_config_path], check=True)
        print("MkDocs serviert die Dokumentation unter http://127.0.0.1:8000")
