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
        print(hierarchy)
        for name, sub_hierarchy in hierarchy.items():
            new_path = os.path.join(base_path, name)
            print(f"Creating directory for component: {name} at {new_path}")
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                logging.info(f"Verzeichnis erstellt: {new_path}")
            self.ensure_files(name, new_path)
            if sub_hierarchy:
                self.create_directories(new_path, sub_hierarchy)

    def ensure_files(self, component_name, component_path):
        required_files = {
            f"{component_name}.cpp": "// C++ source file\n",
            f"{component_name}.hpp": "// C++ header file\n",
            f"{component_name}.md": "# Documentation for {component_name}\n"
        }
        for file_name, content in required_files.items():
            file_path = os.path.join(component_path, file_name)
            if not os.path.exists(file_path):
                self.files.create_component(component_name, component_path) 

    def scan_directory(self, item_path):
        hierarchy = {}
        try:
            for item in os.listdir(item_path):
                full_path = os.path.join(item_path, item)
                if os.path.isdir(full_path):
                    hierarchy[item] = self.scan_directory(full_path)  # Rekursiver Aufruf für Unterverzeichnisse
        except Exception as e:
            print(f"Fehler beim Lesen des Verzeichnisses {item_path}: {e}")
        print(f"Verzeichnisse und Dateien: {hierarchy}")
        return hierarchy

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

