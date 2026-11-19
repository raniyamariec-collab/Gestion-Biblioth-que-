import unittest
from unittest.mock import patch

from service import (
    rechercher_livres,
    emprunter_livre,
    rendre_livre,
    lister_retards,
)


class TestService(unittest.TestCase):

    @patch("service.obtenir_connexion")
    def test_rechercher_livres(self, mock_connexion):
        connexion = mock_connexion.return_value
        connexion.execute.return_value.fetchall.return_value = [
            {
                "id": 1,
                "code": "L001",
                "titre": "Python debutant",
                "auteur": "A. Kone",
            }
        ]

        resultat = rechercher_livres("Python")

        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0]["titre"], "Python debutant")
        connexion.close.assert_called_once()

    @patch("service.obtenir_connexion")
    def test_emprunter_livre_introuvable(self, mock_connexion):
        connexion = mock_connexion.return_value
        connexion.execute.return_value.fetchone.return_value = None

        succes, message = emprunter_livre("INEXISTANT", "ETU001")

        self.assertFalse(succes)
        self.assertEqual(message, "Livre introuvable.")
        connexion.close.assert_called_once()

    @patch("service.obtenir_connexion")
    def test_emprunter_lecteur_introuvable(self, mock_connexion):
        connexion = mock_connexion.return_value
        livre = {
            "id": 1,
            "code": "L001",
            "quantite_disponible": 2,
        }
        connexion.execute.return_value.fetchone.side_effect = [
            livre, None
        ]

        succes, message = emprunter_livre("L001", "INEXISTANT")

        self.assertFalse(succes)
        self.assertEqual(message, "Lecteur introuvable.")
        connexion.close.assert_called_once()

    @patch("service.obtenir_connexion")
    def test_emprunter_sans_exemplaire_disponible(self, mock_connexion):
        connexion = mock_connexion.return_value
        livre = {
            "id": 1,
            "code": "L001",
            "quantite_disponible": 0,
        }
        lecteur = {
            "id": 1,
            "matricule": "ETU001",
        }
        connexion.execute.return_value.fetchone.side_effect = [
            livre, lecteur
        ]

        succes, message = emprunter_livre("L001", "ETU001")

        self.assertFalse(succes)
        self.assertEqual(message, "Aucun exemplaire disponible.")
        connexion.commit.assert_not_called()
        connexion.close.assert_called_once()

    @patch("service.obtenir_connexion")
    def test_emprunter_livre_avec_succes(self, mock_connexion):
        connexion = mock_connexion.return_value
        livre = {
            "id": 1,
            "code": "L001",
            "quantite_disponible": 2,
        }
        lecteur = {
            "id": 1,
            "matricule": "ETU001",
        }
        connexion.execute.return_value.fetchone.side_effect = [
            livre, lecteur
        ]

        succes, message = emprunter_livre("L001", "ETU001")

        self.assertTrue(succes)
        self.assertIn("Emprunt enregistré", message)
        self.assertEqual(connexion.execute.call_count, 4)
        connexion.commit.assert_called_once()
        connexion.close.assert_called_once()

    @patch("service.obtenir_connexion")
    def test_rendre_emprunt_introuvable(self, mock_connexion):
        connexion = mock_connexion.return_value
        connexion.execute.return_value.fetchone.return_value = None

        succes, message = rendre_livre(999999)

        self.assertFalse(succes)
        self.assertEqual(
            message,
            "Emprunt introuvable ou déjà rendu.",
        )
        connexion.close.assert_called_once()

    @patch("service.obtenir_connexion")
    def test_rendre_livre_avec_succes(self, mock_connexion):
        connexion = mock_connexion.return_value
        emprunt = {
            "id": 1,
            "livre_id": 2,
            "date_retour_effective": None,
        }
        connexion.execute.return_value.fetchone.return_value = emprunt

        succes, message = rendre_livre(1)

        self.assertTrue(succes)
        self.assertEqual(message, "Retour enregistré avec succès.")
        self.assertEqual(connexion.execute.call_count, 3)
        connexion.commit.assert_called_once()
        connexion.close.assert_called_once()

    @patch("service.est_en_retard")
    @patch("service.obtenir_connexion")
    def test_lister_retards(self, mock_connexion, mock_retard):
        connexion = mock_connexion.return_value
        connexion.execute.return_value.fetchall.return_value = [
            {
                "id": 1,
                "titre": "Python debutant",
                "date_retour_prevue": "2026-11-01",
            },
            {
                "id": 2,
                "titre": "Algorithmique",
                "date_retour_prevue": "2026-12-01",
            },
        ]
        mock_retard.side_effect = [True, False]

        resultat = lister_retards()

        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0]["id"], 1)
        connexion.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()