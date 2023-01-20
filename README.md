# Aider un enseignant à profiter de ses vacances

## Description
Les enseignants aiment profiter de leurs vacances de façon optimale. L’objectif de ce projet est
d’afficher, pour un enseignant donné, l’intitulé, la date et l’heure de leur dernière intervention
avant chaque période de vacances, ainsi que l’intitulé, la date et l’heure de leur première
intervention après cette période de vacances, ainsi que le nombre exact de jours complets de
vacances dont ils disposent.

## Utilisation
Vous pouvez exécuter le programme avec la commande.
```bash
python3 main.py
```
Il vous sera demandé de renseigner le NOM et PRENOM d'un enseignant, il est important de respecter la nomenclature suivante NOM PRENOM.

Exemple
```bash
DUPONT ANTOINE
```
Vous avez à votre disposition deux script bash.

Le premier permet d'installer les modules nécessaires à l'emploi du programme python
```bash
sh install.sh
```
Il est possible que le programme crée un nombre important de fichier .png et .pdf si il est exécuté plusieurs fois.

Le second script permettra alors de supprimer tout ces fichiers (attention à ne pas glisser de fichier .pdf ou .png dans le dossier avant d'éxecuter la commande auquel cas ces fichiers seraient supprimer)
```bash
sh remove.sh
```
