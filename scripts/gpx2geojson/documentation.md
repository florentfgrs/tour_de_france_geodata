# GPX 2 GeoJSON

## 🎯 Objectif

Le script sert à convertir un fichier GPX en un fichier GeoJSON.

## Utilisation

1. Installer les dépendances du script
2. Éxécuter le script en passant en argument le chemin vers le gpx (ou un dossier contenant des gpx pour uné éxécution en lot).

### Précision concernant l'altitude

- Si tous les points du gpx n'ont pas d'altitude la valeur 0 sera renseigné.
- Si quelques points n'ont pas d'altitude, celle si sera renseigné avec la dernière valeur connu du point précédent.

Pour un gpx :

```sh
python gpx2geojson.py path/to/my_trace.gpx
```

Pour tous les gpx d'un dossier :

```sh
python gpx2geojson.py path/to/my_folder
```
