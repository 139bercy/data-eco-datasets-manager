# ODS API

Outil de monitoring et de pilotage pour la plateforme Data Economie.

## Requirements

Les différents cas d'usage nécessitent une clef de l'API ODS valide, à ajouter au .env (cf. `.env.sample`) 
Merci de vous reporter à la [documentation Opendatasoft](https://help.opendatasoft.com/fr/apis).

## Installation

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip setup.py install
```

## Usage

### Télécharger la liste des datasets

La requête étant un peu lourde, il peut être pertinent d'utiliser le fichier `data/datasets.json` comme source pour 
des traitements réguliers.

```
$ cli datasets download
```

### Formater un output propre en csv

```
$ cli datasets export --exclude-not-published --exclude-restricted --input-file-date "2024-01-01"
```

## Générer un rapport qualité

```
$ python scripts/generate_datasets_quality_export.py
```

Pour vérifier le score d'un jeu de données : 

```
$ cli dataset check-quality -s api -n <dataset_id> --no-dcat
```

