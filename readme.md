# 📍 Tour de France - Geodata

Bienvenue dans le projet **Tour de France - Data Repository** ! Ce dépôt a pour ambition de stocker toutes les données géographiques des parcours des étapes du Tour de France. Que vous soyez un passionné de cyclisme, un data scientist, géomaticien ou simplement curieux de découvrir les tracés des étapes, ce projet est fait pour vous.

## 🏆 Objectifs du projet

- **Collecte des données** : Rassembler les tracés des étapes du Tour de France.
- **Stockage structuré** : Organiser les données de manière à faciliter leur consultation et leur utilisation.
- **Accessibilité** : Mettre à disposition des outils pour accéder facilement aux données et les visualiser.

## 📂 Structure des données dépôt

```bash
Tour-de-France-Data-Repository/
│
├── data/
│   ├── 2023/
│   │   ├── 01
│   │   │   ├── trace_2023_1.geojson
│   │   │   ├── metadata_2023_1.geojson
│   │   ├── 02
│   │   │   ├── trace_2024_1.geojson
│   │   │   ├── metadata_2024_1.geojson
│   └── ...
```

Pour chaque étape il doit y avoir :

- Un fichier [.geojson](https://fr.wikipedia.org/wiki/GeoJSON) :
  - Composé d'une seule et unique entité `Linestring` (et même de préférence `MultiLinestringZ` afin de concerver les informations de dénivellé)
  - Projeté en WGS84 (EPSG:4326)

- Un fichier csv contenu les informations de l'étape et respectant la structure suivante

```csv
numero;date;depart;arrivee;long;denivele
```

| Nom du champ | Description | Exemple |
|--------------|-------------|---------|
| numero       | Numéro de l'étape | 1 |
| date         | Date de l'étape au format JJ/MM/AAAA | 18/05/1993 |
| depart       | Lieu de départ, suivi du code pays au format alpha-3 conformément au standard [ISO 3166-1](https://fr.wikipedia.org/wiki/ISO_3166-1) si cette ville est hors de France. | Laval ou Florence (ITA) |
| arrivee      | Lieu d'arrivée, suivi du code pays au format alpha-3 conformément au standard [ISO 3166-1](https://fr.wikipedia.org/wiki/ISO_3166-1) si cette ville est hors de France. | Laval ou Florence (ITA) |
| long         | Longueur en kilomètre de l'étape (ne prends pas en compte le départ fictif) | 192 |
| denivele     | Dénivelé positif de l'étape en mètre | 541 |

## 🔍 Contenu des dossiers

data/ : Ce dossier contient les fichiers de données géographiques pour chaque étape du Tour de France, organisés par année.
scripts/ : Des scripts Python pour récupérer, traiter et visualiser les données.
notebooks/ : Des notebooks Jupyter pour analyser et visualiser les données.

📝 Contribution
Les contributions sont les bienvenues ! Un fichier CONTRIBUTING.md pour savoir comment procéder sera rédiger sous peu [WIP]

📄 Licence
Ce projet est sous licence GNU GENERAL PUBLIC LICENSE - voir le fichier LICENSE pour plus de détails.

💬 Contact
Pour toute question, n'hésitez pas à ouvrir une issue ou à me contacter.

Merci pour votre intérêt pour ce projet ! 🚴‍♂️💨