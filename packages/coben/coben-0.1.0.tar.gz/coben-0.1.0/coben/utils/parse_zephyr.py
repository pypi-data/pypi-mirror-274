import os
import re

def find_source_files(root_dir, extensions=('.c', '.h')):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extensions):
                yield os.path.join(root, file)

def extract_includes(file_path):
    includes = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'\s*#include\s+["<](.*?)[">]', line)
            if match:
                includes.add(match.group(1))
    return includes
def parse_build_reports(report_paths):
    used_includes = set()
    used_macros = set()
    # Parsen der Reports, um tatsächlich verwendete Includes und Makros zu extrahieren
    # Dummy-Implementierung: Bitte ersetzen Sie dies durch Ihre Logik zum Parsen der Reports
    return used_includes, used_macros

def extract_macros(file_path):
    macros = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r'\s*#define\s+(\w+)', line)
            if match:
                macros.add(match.group(1))
    return macros
def generate_header_file(output_path, includes, macros):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('// Auto-generated header file\n\n')
        for include in sorted(includes):
            file.write(f'#include {include}\n')
        file.write('\n')
        for macro in sorted(macros):
            file.write(f'#define {macro}\n')
def main(source_dir, report_paths, output_header):
    all_includes = set()
    all_macros = set()
    
    for file_path in find_source_files(source_dir):
        all_includes.update(extract_includes(file_path))
        all_macros.update(extract_macros(file_path))
    
    used_includes, used_macros = parse_build_reports(report_paths)
    relevant_includes = all_includes.intersection(used_includes)
    relevant_macros = all_macros.intersection(used_macros)

    generate_header_file(output_header, relevant_includes, relevant_macros)

if __name__ == '__main__':
    source_directory = '/path/to/source'
    report_directory = ['/path/to/ram_report.txt', '/path/to/rom_report.txt']
    output_header = '/path/to/output_header.h'
    main(source_directory, report_directory, output_header)
