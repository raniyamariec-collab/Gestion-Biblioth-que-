import sqlite3
from pathlib import Path


# Chemin du dossier principal du projet
DOSSIER_PROJET = Path(__file__).resolve().parent

# Fichier de la base de données
CHEMIN_BASE = DOSSIER_PROJET / "bibliotheque.db"


def obtenir_connexion():
    """Ouvre une connexion à la base de données SQLite."""
    connexion = sqlite3.connect(CHEMIN_BASE)
    connexion.execute("PRAGMA foreign_keys = ON")
    return connexion


def initialiser_base():
    """Crée les tables de la bibliothèque si elles n'existent pas."""

    connexion = obtenir_connexion()

    try:
        connexion.executescript("""
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                categorie TEXT,
                annee_publication INTEGER,
                quantite_totale INTEGER NOT NULL DEFAULT 1,
                quantite_disponible INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS lecteurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT NOT NULL UNIQUE,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS emprunts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livre_id INTEGER NOT NULL,
                lecteur_id INTEGER NOT NULL,
                date_emprunt TEXT NOT NULL,
                date_retour_prevue TEXT NOT NULL,
                date_retour_effective TEXT,
                FOREIGN KEY (livre_id) REFERENCES livres(id),
                FOREIGN KEY (lecteur_id) REFERENCES lecteurs(id)
            );
        """)

        connexion.commit()
        print("Base de données initialisée avec succès.")

    finally:
        connexion.close()


if __name__ == "__main__":
    initialiser_base()