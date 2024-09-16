#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

DIRECTORY=$1

if [ ! -d "$DIRECTORY" ]; then
  echo "Le dossier $DIRECTORY n'existe pas."
  exit 1
fi

for FILE in "$DIRECTORY"/*.txt;
do
  if [ -e "$FILE" ] && [ "$(basename "$FILE")" != "LISEZ-MOI.txt" ]; then
    mv "$FILE" "${FILE%.txt}.csv"
  fi
done

echo "Changement des fichiers dans le dossier $DIRECTORY effectué."
