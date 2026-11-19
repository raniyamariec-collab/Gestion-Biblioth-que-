BiblioIIT — Gestion de bibliothèque

1. Présentation du projet

BiblioIIT est une application en Python permettant de gérer les opérations principales d'une bibliothèque universitaire depuis une interface en console.

L'application permet de :

- Rechercher des livres par titre, auteur ou code.
- Emprunter un livre.
- Enregistrer le retour d'un livre.
- Consulter la liste des emprunts en retard.

2. Technologies utilisées

- Python 3
- SQLite
- Git et GitHub

SQLite est intégré à Python : aucune installation séparée du serveur SQLite n'est nécessaire.

3. Prérequis

- Avoir Python 3 installé.
- Disposer des fichiers du projet.

4. Installation et exécution

1. Cloner le dépôt GitHub ou télécharger le projet.
2. Ouvrir un terminal dans le dossier du projet.
3. Initialiser la base de données et lancer l'application avec :

python main.py

Le menu principal s'affiche dans le terminal.

5. Données de démonstration

Pour ajouter les livres et les lecteurs de démonstration, exécuter :

python donnees_test.py

Il est recommandé d'exécuter cette commande avant de tester les opérations d'emprunt et de retour.

6. Structure du projet

- "main.py" : point d'entrée de l'application.
- "console.py" : menu et interactions avec l'utilisateur.
- "service.py" : opérations de gestion de la bibliothèque.
- "depot_sqlite.py" : connexion et initialisation de la base de données.
- "modeles.py" : modèles Livre, Lecteur et Emprunt.
- "regles.py" : règles métier, dates de retour et retards.
- "donnees_test.py" : insertion des données de démonstration.
- "bibliotheque.db" : base de données SQLite.

7. Auteur et contribution

Projet réalisé dans le cadre d'un travail pratique de programmation Python.