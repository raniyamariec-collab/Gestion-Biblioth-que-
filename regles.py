from datetime import date, timedelta


DUREE_EMPRUNT = 14


def calculer_date_retour(date_emprunt):
    """Calcule la date limite de retour d'un livre."""
    date_depart = date.fromisoformat(date_emprunt)
    date_retour = date_depart + timedelta(days=DUREE_EMPRUNT)
    return date_retour.isoformat()


def est_en_retard(date_retour_prevue, date_du_jour=None):
    """Vérifie si un emprunt est en retard."""
    if date_du_jour is None:
        date_du_jour = date.today().isoformat()

    return date_du_jour > date_retour_prevue


def livre_disponible(quantite_disponible):
    """Vérifie si au moins un exemplaire est disponible."""
    return quantite_disponible > 0