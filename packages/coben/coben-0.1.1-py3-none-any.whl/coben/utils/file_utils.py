import os
from coben.utils.template_factory import TemplateFactory
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileUtils:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.template_factory = TemplateFactory(self.project_dir)

    def create_component(self, component_name, component_dir):
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

        # Aktualisieren der Elternkomponente
        parent_dir = os.path.dirname(component_dir)
        parent_header_name = f"{os.path.basename(parent_dir)}.hpp" 
        parent_header_path = os.path.join(parent_dir, parent_header_name)

        if os.path.exists(parent_header_path):
            self.update_parent_header(parent_header_path, component_name)
        else:
            logging.error(f"Parent header file not found at {parent_header_path}")

    def update_parent_header(self, parent_header_path, child_component_name):
        with open(parent_header_path, 'r') as file:
            content = file.readlines()

        new_content = []
        for line in content:
            if 'CHILD' in line:
                # Füge die ursprüngliche Zeile mit Kommentaren hinzu
                new_content.append(line)
                # Entferne die Kommentarzeichen und ersetze 'CHILD'
                modified_line = line.replace('//', '').replace('CHILD', child_component_name)
                new_content.append(modified_line)
            else:
                new_content.append(line)

        with open(parent_header_path, 'w') as file:
            file.writelines(new_content)

        print(f"Updated header file at {parent_header_path} with component {child_component_name}")


    def update_parent_component(self, parent_dir, child_name):
        # Zum Beispiel aktualisieren der CMakeLists.txt in der Elternkomponente
        cmake_path = os.path.join(parent_dir, "CMakeLists.txt")
        if os.path.exists(cmake_path):
            with open(cmake_path, 'a') as cmake_file:
                cmake_file.write(f"add_subdirectory({child_name})\n")
                logging.info(f"Updated CMakeLists.txt in {parent_dir} to include {child_name}")
