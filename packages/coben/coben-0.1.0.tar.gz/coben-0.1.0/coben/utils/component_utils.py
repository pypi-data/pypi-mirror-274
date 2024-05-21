import os
import logging
from utils.template_factory import TemplateFactory
from utils.doc_utils import DocumentationManager
from utils.git_utils import GitUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ComponentManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.components_dir = os.path.join(project_dir, "components")
        self.docs_dir = os.path.join(project_dir, "docs")
        self.doc_utils = DocumentationManager(self.project_dir)
        self.template = TemplateFactory(project_dir)
        self.git = GitUtils(self.project_dir)
        self.uml_path = os.path.join(self.docs_dir, f"{project_dir}.puml")
        self.repo_dir = os.path.abspath(self.project_dir)  # Pfad zum Repository-Root


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

    def update_markdown_files(self):
        # os.walk() für rekursives Durchlaufen aller Unterverzeichnisse
        for root, dirs, files in os.walk(self.components_dir):
            for filename in files:
                if filename.endswith('.md'):
                    file_path = os.path.join(root, filename)
                    relative_file_path = os.path.relpath(file_path, self.repo_dir)  # Relativer Pfad zum Repository-Root
                    self.update_markdown_file(file_path, relative_file_path)

    def update_markdown_file(self, file_path, relative_file_path):
        try:
            with open(file_path, 'r+') as file:
                content = file.read()

                # Git-Informationen für die Datei abrufen, die relative Pfadangabe verwenden
                git_info = self.git.get_git_info(relative_file_path)
                for key, value in git_info.items():
                    content = content.replace(f'{{{{ {key} }}}}', value)

                # Zurück zum Anfang der Datei gehen und den geänderten Inhalt schreiben
                file.seek(0)
                file.write(content)
                file.truncate()  # Überschüssigen Inhalt entfernen
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Datei {file_path}: {e}")