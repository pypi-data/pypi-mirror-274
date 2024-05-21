import argparse
from utils.project_setup import ProjectManager
from utils.doc_utils import DocumentationManager
from utils.directory_utils import DirectoryManager
from utils.puml_utils import UMLManager

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description="Verwaltet Projekte.")
    parser.add_argument('command', help='Das auszuführende Kommando: init, build, check, run, monitor, docu, sync')
    parser.add_argument('project_name', help='Name des Projekts')
    return parser.parse_args()

def main():
    args = parse_command_line_arguments()
    print(f"Command: {args.command}, Project Name: {args.project_name}")

    project_manager = ProjectManager(args.project_name)
    doc_manager = DocumentationManager(args.project_name)
    files = DirectoryManager(args.project_name)
    uml = UMLManager(args.project_name)

    if args.command == 'init':
        project_manager.create_project()
    elif args.command == 'build':
        project_manager.build_project()
    elif args.command == 'check':
        project_manager.check_project()
    elif args.command == 'run':
        project_manager.run_project()
    elif args.command == 'monitor':
        project_manager.monitor_project()
    elif args.command == 'docu':
        doc_manager.serve_mkdocs()
    elif args.command == 'sync':
        doc_manager.synchronize_new_markdown()
        uml.sync_uml()
        files.sync_dirs_and_files(uml.parse_hierarchy())
        doc_manager.update_mkdocs_nav(f"{args.project_name}")

if __name__ == "__main__":
    main()

from jinja2 import Environment, FileSystemLoader
import os

class TemplateFactory:
    def __init__(self, project_dir):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, 'templates')
        self.project_dir = project_dir
        self.components_dir = os.path.join(project_dir, "components")
        self.project_name = os.path.basename(os.path.normpath(project_dir))
        self.loader = FileSystemLoader(template_dir)
        self.env = Environment(loader=self.loader)

        self.cpp_template = self.env.get_template('Component.cpp.j2')
        self.hpp_template = self.env.get_template('Component.hpp.j2')
        self.cmake_template = self.env.get_template('CMakeLists.txt.j2')
        self.md_template = self.env.get_template('Component.md.j2')
        self.component_puml_template = self.env.get_template('Component_puml.j2')
        self.project_puml_template = self.env.get_template('project.puml.j2')
        self.ipo_hpp_template = self.env.get_template('ipo.hpp.j2')
        self.ipo_cpp_template = self.env.get_template('ipo.cpp.j2')
        self.cmake_template = self.env.get_template('Project_CMakeLists.txt.j2')
        self.mkdocs_template = self.env.get_template('mkdocs.yml.j2')
        self.main_template = self.env.get_template('main.cpp.j2')
        self.gitignore_template = self.env.get_template('gitignore.j2')
        self.index_template = self.env.get_template('index.md.j2')

    def get_components_content(self, component_name):
        md_content = self.md_template.render(component_name=component_name)
        cmake_content = self.cmake_template.render(component_name=component_name)
        cpp_content = self.cpp_template.render(component_name=component_name)
        hpp_content = self.hpp_template.render(component_name=component_name)
        return md_content, cmake_content, hpp_content, cpp_content

    def get_includes_content(self):
        ipo_hpp_content = self.ipo_hpp_template.render(project_name=self.project_name)
        ipo_cpp_content = self.ipo_cpp_template.render(project_name=self.project_name)
        return ipo_hpp_content, ipo_cpp_content
    def get_project_cmake(self):
        cmake_content = self.cmake_template.render(project_name=self.project_name)
        main_content = self.main_template.render(project_name=self.project_name)
        return cmake_content, main_content
    def get_mkdocs_config(self):
        mkdocs_content = self.mkdocs_template.render(project_name=self.project_name)
        return mkdocs_content
    def get_gitignore(self):
        gitignore_content = self.gitignore_template.render() 
        return gitignore_content
    def get_index_markdown(self):
        index_content = self.index_template.render(project_name=self.project_name)
        return index_content
    def get_project_uml(self):
        uml_content = self.project_puml_template.render(project_name=self.project_name)
        return uml_content
    def get_template(self, template_name):
        return self.env.get_template(template_name)

import os
from utils.template_factory import TemplateFactory
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileUtils:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.template_factory = TemplateFactory(self.project_dir)

    def create_component(self, component_name):
        component_dir = os.path.join(self.project_dir, "components", component_name)
        os.makedirs(component_dir, exist_ok=True)
        templates = {
            'cpp': self.template_factory.get_template('Component.cpp.j2'),
            'hpp': self.template_factory.get_template('Component.hpp.j2'),
            'cmake': self.template_factory.get_template('CMakeLists.txt.j2'),
            'md': self.template_factory.get_template('Component.md.j2')
        }

        file_paths = {
            'cpp': os.path.join(component_dir, f"{component_name}.cpp"),
            'hpp': os.path.join(component_dir, f"{component_name}.hpp"),
            'md': os.path.join(component_dir, f"{component_name}.md"),
            'cmake': os.path.join(component_dir, "CMakeLists.txt")
        }

        for file_type, file_path in file_paths.items():
            with open(file_path, 'w') as f:
                f.write(templates[file_type].render(component_name=component_name))
                logging.info(f"{file_type.upper()} file created at {file_path}")

import os
import logging
from utils.file_utils import FileUtils
from utils.template_factory import TemplateFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DirectoryManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.template_factory = TemplateFactory(self.project_dir)  
        self.components_dir = os.path.join(project_dir, "components")
        self.project_name = os.path.basename(os.path.normpath(project_dir))
        self.files = FileUtils(self.project_dir)

    def create_directories(self, base_path, hierarchy):
        for name, sub_hierarchy in hierarchy.items():
            new_path = os.path.join(base_path, name)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                self.files.create_component()
                logging.info(f"Erstelle Verzeichnis {new_path}")
            elif sub_hierarchy:
                self.create_directories(new_path, sub_hierarchy)

    def create_directories_for_rectangles(self, components_dir, rectangles):
        for rectangle in rectangles:
            dir_path = os.path.join(components_dir, rectangle)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logging.info(f"Verzeichnis für {rectangle} wurde erstellt.")
            else:
                logging.info(f"Verzeichnis für {rectangle} existiert bereits.")

    def update_directories_based_on_changes(self, components_dir, modified_dirs):
        existing_dirs = set(os.listdir(components_dir))
        for mod_dir in modified_dirs:
            if mod_dir not in existing_dirs:
                self.create_directories_for_rectangles(components_dir, [mod_dir])
            else:
                logging.info(f"Keine Veränderung benötigt für: {mod_dir}")

    def create_docs_directories(self, project_dir):
        os.makedirs(f'{project_dir}/docs')

    def sync_dirs_and_files(self, uml_content):
        self.create_directories(self.components_dir, uml_content)

import os
import logging
from utils.template_factory import TemplateFactory
from utils.doc_utils import DocumentationManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ComponentManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.components_dir = os.path.join(project_dir, "components")
        self.docs_dir = os.path.join(project_dir, "docs")
        self.doc_utils = DocumentationManager(self.project_dir)
        self.template = TemplateFactory(project_dir)
        self.uml_path = os.path.join(self.docs_dir, f"{project_dir}.puml")

    def update_cmake_lists(self):
        for root, dirs, files in os.walk(self.components_dir):
            if "CMakeLists.txt" in files and os.path.normpath(root) != os.path.normpath(self.components_dir):
                self.update_single_cmake(root, dirs)

    def update_single_cmake(self, component_dir, subdirs): # kann das nicht auch mit den CmakeLists.txt.j2 geschehen???
        cmake_path = os.path.join(component_dir, "CMakeLists.txt")
        component_name = os.path.basename(component_dir)
        new_content = [
            "cmake_minimum_required(VERSION 3.10)",
            f"project({component_name})",
            f"add_library({component_name}_comp STATIC {component_name}.cpp)",
            f"target_include_directories({component_name}_comp PUBLIC", 
            "${CMAKE_CURRENT_SOURCE_DIR})"
        ]
        if subdirs:
            new_content += [f"add_subdirectory({subdir})\ntarget_link_libraries({component_name}_comp PRIVATE {subdir}_comp)" for subdir in subdirs if os.path.exists(os.path.join(component_dir, subdir, "CMakeLists.txt"))]
        with open(cmake_path, 'w') as cmake_file:
            cmake_file.write("\n".join(new_content) + "\n")
        logging.info(f"CMakeLists.txt in {cmake_path} aktualisiert.")

    def sync_component_docs(self):
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
        for root, dirs, files in os.walk(self.components_dir):
            for file in files:
                if file.endswith('.cpp'):
                    component_name = file[:-4]
                    cmake_path = os.path.join(root, "CMakeLists.txt")
                    linked_components = self.extract_linked_components(cmake_path)
                    self.doc_utils.create_component_markdown(component_name, linked_components, self.env, self.docs_dir)

    def extract_linked_components(self, cmake_path):
        linked_components = []
        try:
            with open(cmake_path, 'r') as file:
                for line in file:
                    if 'add_subdirectory' in line:
                        component = line.split('(')[1].split(')')[0].strip()
                        linked_components.append(component)
        except FileNotFoundError:
            logging.error(f"Die Datei {cmake_path} wurde nicht gefunden.")
        except Exception as e:
            logging.error(f"Fehler beim Lesen der Datei {cmake_path}: {e}")
        return linked_components

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
        path = []
        current = hierarchy

        for line in self.uml_path.splitlines():
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('@enduml'):
                continue
            
            indent = len(line) - len(stripped_line)
            level = indent // 4
            
            if '{' in stripped_line:
                match = re.search(r'\b(class|rectangle)\s+(\w+)', stripped_line)
                if match:
                    element_type, element_name = match.groups()
                    if len(path) == level:
                        current[element_name] = {}
                        path.append(element_name)
                        current = current[element_name]
                    else:
                        while len(path) > level:
                            path.pop()
                            current = hierarchy
                            for step in path:
                                current = current[step]
                        current[element_name] = {}
                        path.append(element_name)
                        current = current[element_name]
            elif '}' in stripped_line:
                if path:
                    path.pop()
                    current = hierarchy
                    for step in path:
                        current = current[step]
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
            uml_components = [f"class {file[:-4]}" for file in files if file.endswith('.hpp')]
            if uml_components:
                component_name = os.path.basename(root)
                uml_code = templates['puml'].render(components=uml_components)
                md_file_path = os.path.join(self.docs_dir, f"{component_name}.md")
                self.append_uml_to_markdown(md_file_path, uml_code)

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

    def update_uml_content(self):
        with open(self.uml_path, 'r') as uml_file:
            content = uml_file.readlines()
        
        start_index = content.index('@startuml\n') + 1
        end_index = content.index('@enduml\n')

        content = content[:start_index] + ['new UML content\n'] + content[end_index:]

        with open(self.uml_path, 'w') as uml_file:
            uml_file.writelines(content)
        logging.info("UML-Datei aktualisiert.")

    def sync_project_diagram(self, project_name):
        modified_dirs = self.get_modified_directories()
        self.update_project_uml(project_name, modified_dirs)
        print(f"Synchronized project diagram for {project_name}")

    def sync_uml(self):
        components = os.listdir(self.components_dir)
        with open(os.path.join(self.project_dir, self.uml_project_file), "w") as uml_file:
            uml_file.write("@startuml\n")
            for component in components:
                if component.endswith(".cpp"):
                    print(f"found component: {component}")
                    uml_file.write(f"component {component[:-4]} as {component}\n")
            uml_file.write("@enduml\n")
        logging.info("UML-Datei aktualisiert.")

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

    def update_mkdocs_nav(self, new_component):
        mkdocs_path = os.path.join(self.project_dir, "mkdocs.yml")
        try:
            with open(mkdocs_path, 'r') as file:
                config = yaml.load(file)
        except FileNotFoundError:
            print(f"Keine mkdocs.yml gefunden in {self.project_dir}. Erstellen Sie eine neue Konfiguration.")
            config = {}
        if 'nav' not in config:
            config['nav'] = [{'Components': new_component}]
        else:
            updated = False
            for item in config['nav']:
                if isinstance(item, dict) and 'Components' in item:
                    item['Components'] = new_component
                    updated = True
                    break
            if not updated:
                config['nav'].append({'Components': new_component})

        with open(mkdocs_path, 'w') as file:
            yaml.dump(config, file)
        print("MkDocs-Konfiguration aktualisiert.")

    def synchronize_new_markdown(self, new_md_files):
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
        self.update_mkdocs_config(new_md_files)
        print("Dokumentation synchronisiert und bereit.")

    def create_new_component_from_markdown(self):
        for md_file in os.listdir(self.docs_dir):
            if md_file.endswith(".md"):
                # Lese die aktuelle UML-Datei und aktualisiere die Inhalte des Markdown
                #with open(os.path.join(project_dir, f"{project_dir}.puml"), "r") as uml_file:
                #    uml_content = uml_file.read()
                self.create_component_markdown(md_file)

    def create_index_md(self):
        index_content = self.template_factory.get_index_markdown()
        index_md_path = os.path.join(self.docs_dir, "index.md")
        with open(index_md_path, 'w') as index_file:
            index_file.write(index_content)

    def serve_mkdocs(self):
        mkdocs_config_path = os.path.join(self.project_dir, "mkdocs.yml")
        subprocess.run(["mkdocs", "serve", "--config-file", mkdocs_config_path], check=True)
        print("MkDocs serviert die Dokumentation unter http://127.0.0.1:8000")

import os
import re
import shutil
import subprocess
import logging
from utils.template_factory import TemplateFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GitUtils:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.template_factory = TemplateFactory()

    def init_git(self):
        subprocess.run(["git", "init"], cwd=self.project_dir)
        gitignore_destination = os.path.join(self.project_dir, '.gitignore')

        gitignore_content = self.template_factory.get_gitignore()
        with open(gitignore_destination, 'w') as gitignore_file:
            gitignore_file.write(gitignore_content)


    def commit_git(self, message):
        subprocess.run(["git", "add", "."], cwd=self.project_dir)
        subprocess.run(["git", "commit", "-m", message], cwd=self.project_dir)
        logging.info(f"Git commit in {self.project_dir} mit Nachricht '{message}'.")

    def create_branch(self, branch_name):
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.project_dir)
        logging.info(f"Neuer Branch {branch_name} in {self.project_dir} erstellt.")

    def get_modified_directories(self):
        result = subprocess.run(
            ["git", "-C", self.project_dir, "status", "--short"],
            capture_output=True, text=True
        )
        modified_dirs = set()
        if result.stdout:
            lines = result.stdout.splitlines()
            for line in lines:
                file_path = line[3:]  # Skip the status code and space (' M ', '?? ', etc.)
                directory = os.path.dirname(file_path)
                if directory:  # Exclude root directory changes
                    modified_dirs.add(directory)
        return modified_dirs

    def get_git_modified_files(self, docs_dir):
        try:
            result = subprocess.run(
                ["git", "-C", self.project_dir, "diff", "--name-only", "--", docs_dir],
                capture_output=True, text=True)
            if result.returncode != 0:
                logging.error(f"Fehler bei der Ausführung von git diff files: {result.stderr}")
                return []
            return [os.path.join(self.project_dir, line) for line in result.stdout.splitlines() if line.strip().endswith(".md")]
        except Exception as e:
            logging.error(f"Ein Fehler ist aufgetreten: {e}")
            return []

    def get_diff_content(self, file_path):
        result = subprocess.run(
            ["git", "-C", self.project_dir, "diff", "HEAD", file_path],
            capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Fehler bei der Ausführung von git diff components: {result.stderr}")
            return ""
        return result.stdout

    def extract_patterns_from_diff(self, diff_content, pattern):
        compiled_pattern = re.compile(pattern)
        return set(compiled_pattern.findall(diff_content))

