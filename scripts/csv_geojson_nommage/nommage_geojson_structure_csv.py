from pathlib import Path
import csv

base_path = Path("path/to/my/repo/tour_de_france_geodata/data")

def is_correctly_named(file, year, step):
    expected_name = f"trace_{year}_{step}.geojson"
    return file.name == expected_name

def create_metadata_file(step_dir, year, step):
    metadata_filename = f"metadata_{year}_{step}.csv"
    metadata_path = step_dir / metadata_filename
    if not metadata_path.exists():
        with metadata_path.open('w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['numero', 'date', 'depart', 'arrivee', 'long', 'denivele', 'type', 'wiki'])
        print(f"Fichier de métadonnées créé : {metadata_path}")
    else:
        print(f"Fichier de métadonnées existe déjà : {metadata_path}")

for year_dir in base_path.iterdir():
    if year_dir.is_dir() and year_dir.name.isdigit():
        year = year_dir.name
        for step_dir in year_dir.iterdir():
            if step_dir.is_dir() and step_dir.name.isdigit():
                step = int(step_dir.name)
                for file in step_dir.iterdir():
                    if file.is_file() and file.suffix == '.geojson':
                        if not is_correctly_named(file, year, step):
                            new_name = f"trace_{year}_{step}.geojson"
                            new_path = step_dir / new_name
                            file.rename(new_path)
                            print(f"Renommé {file} en {new_path}")
                        else:
                            print(f"{file} est déjà correctement nommé")
                create_metadata_file(step_dir, year, step)
