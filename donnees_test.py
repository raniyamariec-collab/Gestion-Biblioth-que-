from depot_sqlite import obtenir_connexion


def ajouter_donnees_test():
    connexion = obtenir_connexion()

    try:
        livres = [
            ("L001", "Les Misérables", "Victor Hugo", "Roman", 1862, 3, 3),
            ("L002", "L'Etranger", "Albert Camus", "Roman", 1942, 2, 2),
            ("L003", "Python pour débutants", "John Smith", "Informatique", 2023, 4, 4),
            ("L004", "Le Petit Prince", "Antoine de Saint-Exupéry", "Conte", 1943, 3, 3),
            ("L005", "Une si longue lettre", "Mariama Bâ", "Roman", 1979, 2, 2),
            ("L006", "L'Aventure ambiguë", "Cheikh Hamidou Kane", "Roman", 1961, 2, 2),
            ("L007", "Candide", "Voltaire", "Philosophie", 1759, 2, 2),
            ("L008", "Germinal", "Émile Zola", "Roman", 1885, 3, 3),
            ("L009", "Le Rouge et le Noir", "Stendhal", "Roman", 1830, 2, 2),
            ("L010", "Les Fleurs du mal", "Charles Baudelaire", "Poésie", 1857, 2, 2),
            ("L011", "Introduction à l'algorithmique", "Thomas Cormen", "Informatique", 2009, 3, 3),
            ("L012", "Apprendre le langage C", "Jean Dupont", "Informatique", 2022, 3, 3),
            ("L013", "Bases de données", "Abraham Silberschatz", "Informatique", 2019, 2, 2),
            ("L014", "Réseaux informatiques", "Andrew Tanenbaum", "Informatique", 2021, 2, 2),
            ("L015", "Clean Code", "Robert C. Martin", "Informatique", 2008, 2, 2),
            ("L016", "L'Art de la guerre", "Sun Tzu", "Stratégie", -500, 2, 2),
            ("L017", "Le Monde s'effondre", "Chinua Achebe", "Roman", 1958, 2, 2),
            ("L018", "Le Vieil Homme et la Mer", "Ernest Hemingway", "Roman", 1952, 2, 2),
            ("L019", "Sapiens", "Yuval Noah Harari", "Histoire", 2011, 2, 2),
            ("L020", "L'Alchimiste", "Paulo Coelho", "Roman", 1988, 3, 3),
        ]

        etudiants = [
            ("ETU001", "Kouassi", "Marie"),
            ("ETU002", "Yao", "Paul"),
            ("ETU003", "Konan", "Aminata"),
            ("ETU004", "Koffi", "Jean"),
            ("ETU005", "Traore", "Fatou"),
            ("ETU006", "Diallo", "Ibrahim"),
            ("ETU007", "Bamba", "Awa"),
            ("ETU008", "N'Guessan", "Kevin"),
            ("ETU009", "Toure", "Mariam"),
            ("ETU010", "Kone", "Abdou"),
        ]

        connexion.executemany(
            """
            INSERT OR IGNORE INTO livres
            (code, titre, auteur, categorie, annee_publication,
             quantite_totale, quantite_disponible)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            livres,
        )

        connexion.executemany(
            """
            INSERT OR IGNORE INTO lecteurs (matricule, nom, prenom)
            VALUES (?, ?, ?)
            """,
            etudiants,
        )

        connexion.commit()
        print("20 livres et 10 étudiants ajoutés ou déjà présents.")

    except Exception:
        connexion.rollback()
        raise

    finally:
        connexion.close()


if __name__ == "__main__":
    ajouter_donnees_test()