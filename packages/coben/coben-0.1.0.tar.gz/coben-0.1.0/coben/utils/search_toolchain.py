import os
import glob

def find_toolchain_files(start_dir):
    """
    Durchsucht rekursiv das angegebene Verzeichnis und alle Unterverzeichnisse
    nach Dateien, die auf 'toolchain*.cmake' passen.

    :param start_dir: Der Startordner, von dem aus die Suche beginnen soll.
    :return: Eine Liste von Pfaden zu gefundenen Toolchain-Dateien.
    """
    # Erstelle eine leere Liste, um die Pfade der gefundenen Toolchain-Dateien zu speichern
    toolchain_files = []
    
    # Durchlaufe alle Verzeichnisse beginnend bei start_dir
    for root, dirs, files in os.walk(start_dir):
        # Finde alle '.cmake' Dateien, die 'toolchain' im Namen haben
        for file in files:
            if 'toolchain' in file and file.endswith('.cmake'):
                # Füge den vollständigen Pfad zur Liste hinzu
                toolchain_files.append(os.path.join(root, file))
    
    return toolchain_files

# Beispielaufruf der Funktion
if __name__ == "__main__":
    start_directory = '/'  # Ändern Sie dies zu einem spezifischen Startverzeichnis auf Ihrem System
    found_toolchains = find_toolchain_files(start_directory)
    print("Gefundene Toolchain-Dateien:")
    for toolchain in found_toolchains:
        print(toolchain)
