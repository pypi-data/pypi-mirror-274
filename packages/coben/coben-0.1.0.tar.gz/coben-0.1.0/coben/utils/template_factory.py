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
        self.component_cmake_template = self.env.get_template('CMakeLists.txt.j2')
        self.md_template = self.env.get_template('Component.md.j2')
        self.component_puml_template = self.env.get_template('Component.puml.j2')
        self.project_puml_template = self.env.get_template('project.puml.j2')
        self.ipo_hpp_template = self.env.get_template('ipo.hpp.j2')
        self.ipo_cpp_template = self.env.get_template('ipo.cpp.j2')
        self.project_cmake_template = self.env.get_template('Project_CMakeLists.txt.j2')
        self.mkdocs_template = self.env.get_template('mkdocs.yml.j2')
        self.main_template = self.env.get_template('main.cpp.j2')
        self.gitignore_template = self.env.get_template('gitignore.j2')
        self.index_template = self.env.get_template('index.md.j2')

    def get_components_content(self, component_name):
        md_content = self.md_template.render(component_name=component_name)
        cmake_content = self.component_cmake_template.render(component_name=component_name)
        cpp_content = self.cpp_template.render(component_name=component_name)
        hpp_content = self.hpp_template.render(component_name=component_name)
        return md_content, cmake_content, hpp_content, cpp_content

    def get_includes_content(self):
        ipo_hpp_content = self.ipo_hpp_template.render(project_name=self.project_name)
        ipo_cpp_content = self.ipo_cpp_template.render(project_name=self.project_name)
        return ipo_hpp_content, ipo_cpp_content
    def get_project_cmake(self, platform):
        toolchain_path = {
            'esp32': '$IDF_PATH/tools/cmake/toolchain-esp32.cmake',
            'arm64': '/path/to/arm64/toolchain.cmake',
            'rm2': '/home/dieter/own/rm2/toolchain.cmake',
            'plain': ''
        }.get(platform, '') 

        cmake_content = self.project_cmake_template.render(project_name=self.project_name, platform_name=toolchain_path)
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

