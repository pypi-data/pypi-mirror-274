import argparse
import os
from utils.project_setup import ProjectManager
from utils.doc_utils import DocumentationManager
from utils.directory_utils import DirectoryManager
from utils.puml_utils import UMLManager
from utils.git_utils import GitUtils
from utils.component_utils import ComponentManager

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description="Verwaltet Projekte.")
    parser.add_argument('command', help='Das auszuführende Kommando: init, build, check, run, monitor, docu, sync, from-dirs')
    parser.add_argument('--platform', help='Zielplattform für das Build: plain, esp32, arm64, etc.', default=None)
    parser.add_argument('project_name', help='Name des Projekts')
    return parser.parse_args()

def main():
    args = parse_command_line_arguments()
    print(f"Command: {args.command}, Project Name: {args.project_name}")

    if args.command == 'init' and args.platform is None:
        print("Error: 'init' command requires the 'platform' argument.")
        return

    if args.platform:
        print(f"Platform: {args.platform}")

    project_manager = ProjectManager(args.project_name, args.platform)
    doc_manager = DocumentationManager(args.project_name)
    files = DirectoryManager(args.project_name)
    uml = UMLManager(args.project_name)
    git = GitUtils(args.project_name)
    components_update = ComponentManager(args.project_name)
    
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
    elif args.command == 'from-dirs':
        # TODO: fix: wenn kein verzeichnis da ist, wird es im projekt.puml gelöscht.
        component_dir = os.path.join(args.project_name, 'components')
        uml.update_uml_file(files.scan_directory(component_dir))
        uml.sync_uml()
        doc_manager.update_mkdocs_nav(uml.parse_hierarchy())
        components_update.update_markdown_files()
        git.commit_git("sync project from directories")
    elif args.command == 'sync':
        uml.sync_uml()
        files.sync_dirs_and_files(uml.parse_hierarchy())
        doc_manager.update_mkdocs_nav(uml.parse_hierarchy())
        components_update.update_markdown_files()
        git.commit_git("sync project from UML")

if __name__ == "__main__":
    main()
