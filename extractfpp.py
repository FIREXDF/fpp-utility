import zipfile
import json
import os

def extract_fpp(filename, output_directory):
    """Extrait un FightPlannerPackage (.fpp) en conservant les fichiers et dossiers vides."""
    with zipfile.ZipFile(filename, 'r') as fpp:
        # Lire le manifest du fichier .fpp
        manifest = json.loads(fpp.read("manifest.json"))
        
        print("\n📦 FightPlannerPackage détecté !")
        print("🔹 Version :", manifest["version"])
        print("📂 Fichiers contenus :")
        for file in manifest["files"]:
            print(f"  - {file}")
        
        print("📁 Dossiers inclus :")
        for dir_path in manifest["directories"]:
            print(f"  - {dir_path}")
        
        # Extraction des fichiers
        fpp.extractall(output_directory)  # Extraire les fichiers dans le dossier de destination

        # Création des dossiers vides (si nécessaire)
        for dir_path in manifest["directories"]:
            dir_full_path = os.path.join(output_directory, "data", dir_path)
            os.makedirs(dir_full_path, exist_ok=True)  # Crée le dossier vide s'il n'existe pas

        print(f"\n✅ Fichiers extraits dans '{output_directory}'")

# 🔹 Demande le nom du fichier .fpp à extraire
nom_fichier = input("Entrez le nom du fichier .fpp à extraire (avec extension) : ")
extract_fpp(nom_fichier, "extraction")  # Dossier d'extraction par défaut : 'extraction'
