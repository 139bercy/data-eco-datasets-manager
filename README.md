# ODS API

Premiers scripts de gestion de la plateforme Data Eco avec l'API ODS. 

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
$ cli api get-datasets
```

## Générer un rapport qualité

```
$ python scripts/generate_datasets_quality_export.py
```

