import argparse
import gpxpy
import geojson

def gpx_to_geojson(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    if gpx.tracks:
        track = gpx.tracks[0]
        points = []
        
        for segment in track.segments:
            for point in segment.points:
                points.append((point.longitude, point.latitude))

        linestring = geojson.LineString(points)

        feature = geojson.Feature(geometry=linestring, properties={}, id="track", crs={"type": "name", "properties": {"name": "EPSG:4326"}})

        feature_collection = geojson.FeatureCollection([feature])

        with open(gpx_file_path.replace(".gpx", ".geojson"), 'w') as geojson_file:
            geojson.dump(feature_collection, geojson_file, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Convertir un fichier GPX en fichier GeoJSON.")
    parser.add_argument('gpx_file', help="Chemin du fichier GPX à convertir")
    args = parser.parse_args()

    gpx_to_geojson(args.gpx_file)

if __name__ == "__main__":
    main()