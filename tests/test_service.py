import unittest
from unittest.mock import patch
from service import rechercher_livres, emprunter_livre


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


if __name__ == "__main__":
    unittest.main()