import zipfile
import json
import os

def get_all_files_and_dirs(directory):
    """Récupère récursivement tous les fichiers et dossiers du dossier `mods/`."""
    file_list = []
    dir_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, directory)
            file_list.append((full_path, relative_path))

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            rel_dir_path = os.path.relpath(dir_path, directory)
            dir_list.append(rel_dir_path)  # Ajoute les dossiers pour qu'ils soient inclus

    return file_list, dir_list

def create_fpp(output_filename, input_directory="mods"):
    """Crée un fichier FightPlannerPackage (.fpp) incluant tous les fichiers et dossiers (vides ou non)."""
    if not os.path.exists(input_directory):
        print(f"❌ Erreur : le dossier '{input_directory}' n'existe pas.")
        return

    files, dirs = get_all_files_and_dirs(input_directory)

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as fpp:
        # Création du manifest
        manifest = {
            "version": 1,
            "files": [rel_path for _, rel_path in files],
            "directories": dirs  # On ajoute aussi les dossiers
        }
        fpp.writestr("manifest.json", json.dumps(manifest, indent=2))

        # Ajout des fichiers en conservant leur structure
        for full_path, rel_path in files:
            fpp.write(full_path, f"data/{rel_path}")

        # Ajout des dossiers vides en créant des entrées ZIP
        for dir_path in dirs:
            fpp.writestr(f"data/{dir_path}/", "")  # Crée un dossier vide dans l'archive

    print(f"\n✅ FightPlannerPackage créé : {output_filename}")
    print("📂 Fichiers inclus :")
    for _, rel_path in files:
        print(f"  - {rel_path}")
    print("📁 Dossiers inclus (y compris vides) :")
    for dir_path in dirs:
        print(f"  - {dir_path}")

# 🔹 Demande un nom pour le fichier .fpp
nom_fichier = input("Entrez le nom du fichier .fpp (sans extension) : ") + ".fpp"
create_fpp(nom_fichier)
