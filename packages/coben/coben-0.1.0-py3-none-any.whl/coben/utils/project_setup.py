import os
import subprocess
import psutil
from utils.template_factory import TemplateFactory
from utils.git_utils import GitUtils
from utils.component_utils import ComponentManager
from utils.doc_utils import DocumentationManager
from utils.puml_utils import UMLManager

class ProjectManager:
    def __init__(self, project_name, platform):
        self.project_name = project_name
        self.platform = platform
        self.project_dir = os.path.join(os.getcwd(), project_name)
        self.template_factory = TemplateFactory(self.project_dir)
        self.components = ComponentManager(self.project_dir)
        self.documents = DocumentationManager(self.project_name)
        self.git_utils = GitUtils(self.project_dir) 
        self.uml = UMLManager(self.project_dir)

    def setup_build_environment(self):
        cmake_content, main_content = self.template_factory.get_project_cmake(self.platform)
        with open(os.path.join(self.project_dir, 'CMakeLists.txt'), 'w') as file:
            file.write(cmake_content)
        with open(os.path.join(self.project_dir, 'main.cpp'), 'w') as file:
            file.write(main_content)
        
        if self.platform == 'esp32' and 'IDF_PATH' not in os.environ:
            os.environ['IDF_PATH'] = '/path/to/esp-idf'

    def initialize_project_directory(self):
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)
        self.setup_build_environment()
        print(f"Projektdateien für {self.project_name} erstellt.")

    def initialize_documentation_config(self):
        mkdocs_content=self.template_factory.get_mkdocs_config()
        with open(os.path.join(self.project_dir, 'mkdocs.yml'), 'w') as file:
            file.write(mkdocs_content)

    def create_components_directory_and_files(self):
        component_dir = os.path.join(self.project_dir, 'components', self.project_name)
        os.makedirs(component_dir, exist_ok=True)

        md_content, cmake_content, hpp_content, cpp_content = self.template_factory.get_components_content(self.project_name)

        with open(os.path.join(component_dir, f"{self.project_name}.cpp"), 'w') as cpp_file:
            cpp_file.write(cpp_content)
        with open(os.path.join(component_dir, f"{self.project_name}.hpp"), 'w') as hpp_file:
            hpp_file.write(hpp_content)
        with open(os.path.join(component_dir, 'CMakeLists.txt'), 'w') as file:
            file.write(cmake_content)
        with open(os.path.join(component_dir, f"{self.project_name}.md"), 'w') as hpp_file:
            hpp_file.write(md_content)

    def create_include_directory_and_files(self):
        include_dir = os.path.join(self.project_dir, 'include')
        os.makedirs(include_dir, exist_ok=True)
        ipo_hpp_content, ipo_cpp_content = self.template_factory.get_includes_content()

        with open(os.path.join(include_dir, 'ipo.hpp'), 'w') as hpp_file:
            hpp_file.write(ipo_hpp_content)
        with open(os.path.join(include_dir, 'ipo.cpp'), 'w') as cpp_file:
            cpp_file.write(ipo_cpp_content)

    def build_project(self):
        build_dir = os.path.join(self.project_dir, 'build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        subprocess.run(["cmake", ".."], cwd=build_dir)
        subprocess.run(["make"], cwd=build_dir)
        if self.check_build_success():
            print("Build war erfolgreich, starte Analysen...")
            self.analyze_binary_size()
            self.perform_static_analysis()
            self.schedule_dynamic_analysis()
        else:
            print("Build fehlgeschlagen, keine Analyse möglich.") 

    def run_project(self):
        build_dir = os.path.join(self.project_dir, 'build')
        subprocess.run([f"./main"], cwd=build_dir)
        print("Anwendung wird ausgeführt.")

    def run_command(self, command):
        """Hilfsfunktion zum Ausführen von Shell-Befehlen innerhalb der Klasse"""
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Ausführen von {command}: {e.stderr}")
            return None

    def check_build_success(self):
        build_dir = os.path.join(self.project_dir, 'build')
        return os.path.exists(os.path.join(build_dir, 'main'))

    def analyze_binary_size(self):
        """Analysiert die Größe des Binärs"""
        print("Analysiere die Binärgröße...")
        build_dir = os.path.join(self.project_dir, 'build')
        executable_path =os.path.join(build_dir, 'main')
        file_size_output = self.run_command(['ls', '-l', executable_path])
        print(file_size_output)
        size_output = self.run_command(['size', executable_path])
        print(size_output)

    def perform_static_analysis(self):
        """Führt statische Codeanalyse durch"""
        print("Führe statische Codeanalyse durch...")
        cppcheck_output = self.run_command(['cppcheck', '--enable=all', '--std=c++17', self.project_dir])
        print(cppcheck_output)

    def schedule_dynamic_analysis(self):
        """Plant dynamische Analyse für später (dies erfordert manuellen Eingriff oder Testskripte)"""
        build_dir = os.path.join(self.project_dir, 'build')
        executable_path =os.path.join(build_dir, 'main')
        print(f"Bitte führen Sie Valgrind oder Sanitizer für {executable_path} aus, um die dynamische Analyse zu vervollständigen.")


    def monitor_project(self):
        build_dir = os.path.join(self.project_dir, 'build')
        process = subprocess.Popen([f"./{self.project_name}"], cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            while True:
                p = psutil.Process(process.pid)
                cpu_usage = p.cpu_percent(interval=1)
                memory_usage = p.memory_info().rss
                print(f"CPU-Nutzung: {cpu_usage}%, Speichernutzung: {memory_usage} bytes")
        except psutil.NoSuchProcess:
            print("Prozess beendet.")
        except KeyboardInterrupt:
            print("Monitoring abgebrochen.")
        finally:
            process.kill()

    def create_project(self):
        self.initialize_project_directory()
        self.git_utils.init_git()  
        self.initialize_documentation_config()
        self.create_components_directory_and_files()
        self.create_include_directory_and_files()
        self.build_project() 

        self.uml.create_project_uml()
        self.documents.create_index_md()
        self.git_utils.commit_git("Initial commit")  
        print(f"Projekt {self.project_name} wurde eingerichtet und ist bereit für die Entwicklung.")

