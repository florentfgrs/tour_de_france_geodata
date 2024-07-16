# Scrapwiki

## 🎯 Objectif

L'objectif de ce script est de récupéré les informations contenu dans le fichier CSV depuis les pages wikipédia des étapes.
Puis de traiter ces informations pour les convertir au format attendu. Attention le code iso-3 de pays n'a pas été automatisé. Si départ à l'étranger il faut modifier à la mano.
Attention également à bien créer la sctructure des csv aupravant avec le script `nommage_geojson_structure_csv.py` (TODO automatiser cela dans ce script).

Ce script prends deux arguments :

- L'année
-Le nombre d'étapes

## Utilisation

Exemple pour 2023, 21 étapes.

```sh
python3 scripts/scrapwiki/webscrapping_wiki.py 2023 21
```
