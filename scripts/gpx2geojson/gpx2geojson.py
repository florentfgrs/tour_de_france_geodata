import argparse
import gpxpy
import geojson
from pathlib import Path

def gpx_to_geojson(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    if gpx.tracks:
        track = gpx.tracks[0]
        linestrings = []
        
        for segment in track.segments:
            points = []
            last_elevation = 0  # Utiliser une valeur par défaut au début
            # Si une altitude est inconu on utilise l'altitude du dernier point connu
            for point in segment.points:
                if point.elevation is not None:
                    last_elevation = point.elevation
                points.append((point.longitude, point.latitude, last_elevation))
            linestrings.append(points)
        
        multi_linestring = geojson.MultiLineString(linestrings)

        feature = geojson.Feature(geometry=multi_linestring, properties={}, id="track", crs={"type": "name", "properties": {"name": "EPSG:4326"}})

        feature_collection = geojson.FeatureCollection([feature])

        output_name = str(gpx_file_path).replace(".gpx", ".geojson")

        with open(output_name, 'w') as geojson_file:
            geojson.dump(feature_collection, geojson_file, indent=2)
def process_directory(directory_path):
    folder_path = Path(directory_path)
    if folder_path.is_dir():
        for file_path in folder_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == '.gpx':
                print(f"Processing file: {file_path}")
                gpx_to_geojson(file_path)

def main():
    parser = argparse.ArgumentParser(description="Convertir un fichier GPX ou tous les fichiers GPX d'un dossier en fichiers GeoJSON.")
    parser.add_argument('path', help="Chemin du fichier GPX ou du dossier contenant les fichiers GPX à convertir")
    args = parser.parse_args()

    path = Path(args.path)
    if path.is_file():
        gpx_to_geojson(path)
    elif path.is_dir():
        process_directory(path)
    else:
        print(f"Le chemin {path} n'est ni un fichier ni un dossier valide.")

if __name__ == "__main__":
    main()