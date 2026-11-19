import unittest
from regles import (
    calculer_date_retour,
    est_en_retard,
    livre_disponible,
)


class TestRegles(unittest.TestCase):

    def test_calculer_date_retour(self):
        resultat = calculer_date_retour("2026-11-01")
        self.assertEqual(resultat, "2026-11-15")

    def test_est_en_retard(self):
        resultat = est_en_retard(
            "2026-11-10",
            "2026-11-19"
        )
        self.assertTrue(resultat)

    def test_livre_disponible(self):
        self.assertTrue(livre_disponible(2))
        self.assertFalse(livre_disponible(0))


if __name__ == "__main__":
    unittest.main()