from datetime import date

from depot_sqlite import obtenir_connexion
from regles import (
    calculer_date_retour,
    est_en_retard,
    livre_disponible,
)

def rechercher_livres(mot_cle):
    """Recherche un livre par son titre, son auteur ou son code."""
    connexion = obtenir_connexion()

    try:
        connexion.row_factory = __import__("sqlite3").Row

        curseur = connexion.execute(
            """
            SELECT * FROM livres
            WHERE titre LIKE ? OR auteur LIKE ? OR code LIKE ?
            ORDER BY titre
            """,
            (f"%{mot_cle}%", f"%{mot_cle}%", f"%{mot_cle}%"),
        )

        livres = curseur.fetchall()
        return [dict(livre) for livre in livres]

    finally:
        connexion.close()



def emprunter_livre(code_livre, matricule):
    """Enregistre l'emprunt d'un livre par un lecteur."""
    connexion = obtenir_connexion()

    try:
        connexion.row_factory = __import__("sqlite3").Row

        livre = connexion.execute(
            "SELECT * FROM livres WHERE code = ?",
            (code_livre,),
        ).fetchone()

        lecteur = connexion.execute(
            "SELECT * FROM lecteurs WHERE matricule = ?",
            (matricule,),
        ).fetchone()

        if livre is None:
            return False, "Livre introuvable."

        if lecteur is None:
            return False, "Lecteur introuvable."

        if not livre_disponible(livre["quantite_disponible"]):
            return False, "Aucun exemplaire disponible."

        aujourdhui = date.today().isoformat()
        date_limite = calculer_date_retour(aujourdhui)

        connexion.execute(
            """
            INSERT INTO emprunts
            (livre_id, lecteur_id, date_emprunt, date_retour_prevue)
            VALUES (?, ?, ?, ?)
            """,
            (livre["id"], lecteur["id"], aujourdhui, date_limite),
        )

        connexion.execute(
            """
            UPDATE livres
            SET quantite_disponible = quantite_disponible - 1
            WHERE id = ?
            """,
            (livre["id"],),
        )

        connexion.commit()
        return True, f"Emprunt enregistré. Retour prévu le {date_limite}."

    except Exception:
        connexion.rollback()
        raise
    finally:
        connexion.close()


def rendre_livre(id_emprunt):
    """Enregistre le retour d'un livre emprunté."""
    connexion = obtenir_connexion()

    try:
        connexion.row_factory = __import__("sqlite3").Row

        emprunt = connexion.execute(
            """
            SELECT * FROM emprunts
            WHERE id = ? AND date_retour_effective IS NULL
            """,
            (id_emprunt,),
        ).fetchone()

        if emprunt is None:
            return False, "Emprunt introuvable ou déjà rendu."

        aujourdhui = date.today().isoformat()

        connexion.execute(
            """
            UPDATE emprunts
            SET date_retour_effective = ?
            WHERE id = ?
            """,
            (aujourdhui, id_emprunt),
        )

        connexion.execute(
            """
            UPDATE livres
            SET quantite_disponible = quantite_disponible + 1
            WHERE id = ?
            """,
            (emprunt["livre_id"],),
        )

        connexion.commit()
        return True, "Retour enregistré avec succès."

    except Exception:
        connexion.rollback()
        raise
    finally:
        connexion.close()


def lister_retards():
    """Liste les emprunts non rendus dont la date limite est dépassée."""
    connexion = obtenir_connexion()

    try:
        connexion.row_factory = __import__("sqlite3").Row

        emprunts = connexion.execute(
            """
            SELECT emprunts.*, livres.titre,
                   lecteurs.nom, lecteurs.prenom, lecteurs.matricule
            FROM emprunts
            JOIN livres ON emprunts.livre_id = livres.id
            JOIN lecteurs ON emprunts.lecteur_id = lecteurs.id
            WHERE emprunts.date_retour_effective IS NULL
            ORDER BY emprunts.date_retour_prevue
            """
        ).fetchall()

        return [
            dict(emprunt)
            for emprunt in emprunts
            if est_en_retard(emprunt["date_retour_prevue"])
        ]
    finally:
        connexion.close()