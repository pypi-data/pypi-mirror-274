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
        self.template_factory = TemplateFactory(self.project_dir)

    def init_git(self):
        subprocess.run(["git", "init"], cwd=self.project_dir)
        gitignore_destination = os.path.join(self.project_dir, '.gitignore')

        gitignore_content = self.template_factory.get_gitignore()
        with open(gitignore_destination, 'w') as gitignore_file:
            gitignore_file.write(gitignore_content)

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

    def get_git_status(self):
        status = subprocess.check_output(['git', 'status'], text=True)
        return status
    
    def get_git_info(self, file_path):
        try:
            # Befehl um das letzte Änderungsdatum zu bekommen
            date_command = ['git', '-C', self.project_dir, 'log', '-1', '--format=%ad', '--', file_path]
            last_commit_date = subprocess.check_output(date_command, text=True).strip()

            # Befehl um den letzten Commit Hash zu bekommen
            hash_command = ['git', '-C', self.project_dir, 'log', '-1', '--format=%H', '--', file_path]
            last_commit_hash = subprocess.check_output(hash_command, text=True).strip()

            # Befehl um den Autor des letzten Commits zu bekommen
            author_command = ['git', '-C', self.project_dir, 'log', '-1', '--format=%an', '--', file_path]
            author = subprocess.check_output(author_command, text=True).strip()

            gitinfo = {'commit_hash': last_commit_hash, 'author': author, 'date': last_commit_date}
            return gitinfo
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Ausführen von Git-Befehl: {e}")
            return None
    
    def commit_git(self, message):
        message = f"{message} at directories: {self.get_modified_directories()}"
        subprocess.run(["git", "add", "."], cwd=self.project_dir)
        subprocess.run(["git", "commit", "-m", message], cwd=self.project_dir)
        logging.info(f"Git commit in {self.project_dir} mit Nachricht '{message}'.")

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
