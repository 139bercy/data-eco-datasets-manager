
Quelles sont les API utilisées : 
- API Automation pour récupérer la liste des datasets
- API Explore pour récupérer le détail des datasets

Les données peuvent provenir de plusieurs sources : 
- Directement de l'API
- De fichiers JSON
- De fichiers CSV

Les données peuvent être exportées via : 
- Fichier CSV
- Base de données PostgreSQL
- Base de données SQLite

## Quality score

Les fichiers comprenant test dans le jeu de données ou le `dataset_id`
- Doivent être préfixés `test-*`
- Doivent être en accès restreint

## Données supplémentaires

metas > default > records_count
metas > processing > records_size
metas > explore > reuse_count
metas > explore > download_count
metas > explore > api_call_count
metas > explore > popularity_score

## TODOS

TODO: Rationaliser la gestion des noms de fichier (I/O) sur l'ensemble de l'application. 
TODO: Ne pas prendre en compte les jeux de données non mis à jour depuis le dernier passage 

## Ideas

Fonctionnalités : 
- Ajouter une notion d'historique pour voir l'évolution de la qualité du jeu de données dans le temps.

Refactor: 
- Ajouter les ports et adapters prenant en compte les sources (import et export)