# Data to BDD

## 🎯 Objectif

L'objetcif est de fournir un script afin d'importer les données de ce repo dans une base de données géographique.

Une table par année sera créé. Dans chaque table une entité correpond à une étape. Pour chaque entité on retrouve la geometrie provenant du `GeoJSON` ainsi ainsi que les informations attributaires fournies par le fichier `metadata_AAAA_E.csv`.

Il existe deux scripts pour deux systèmes de bases de données géographiques (avec chacun leurs aruguments):

- PostgreSQL/PostGIS
- DuckDB
  - argument 1 : chemin de la base de données (existante ou a créer)
  - argument 2 : chemin vers le dossier data du reportoire git

## Utilisation

```sh
python ./scripts/data2bdd/data2duckdb.py path/to/my_bdd.db path/to/repo/tour_de_france_geodata/data
```
