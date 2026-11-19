from service import (
    rechercher_livres,
    emprunter_livre,
    rendre_livre,
    lister_retards,
)


def afficher_menu():
    print("\n=== Gestion BiblioIIT ===")
    print("Bienvenue dans la biblotheque de IIT ")
    print("1. Rechercher un livre")
    print("2. Emprunter")
    print("3. Rendre")
    print("4. Retards")
    print("0. Quitter")


def rechercher():
    mot_cle = input("Titre, auteur ou code du livre : ").strip()
    livres = rechercher_livres(mot_cle)

    if not livres:
        print("Aucun livre trouvé.")
        return

    for livre in livres:
        print(
            f"Code : {livre['code']} | "
            f"Titre : {livre['titre']} | "
            f"Auteur : {livre['auteur']} | "
            f"Disponibles : {livre['quantite_disponible']}"
        )


def emprunter():
    code = input("Code du livre : ").strip()
    matricule = input("Matricule du lecteur : ").strip()

    succes, message = emprunter_livre(code, matricule)
    print(message)


def rendre():
    try:
        id_emprunt = int(input("Identifiant de l'emprunt : "))
    except ValueError:
        print("Veuillez saisir un identifiant numérique.")
        return

    succes, message = rendre_livre(id_emprunt)
    print(message)


def afficher_retards():
    retards = lister_retards()

    if not retards:
        print("Aucun retard enregistré.")
        return

    for emprunt in retards:
        print(
            f"Emprunt n°{emprunt['id']} | "
            f"Livre : {emprunt['titre']} | "
            f"Lecteur : {emprunt['nom']} {emprunt['prenom']} | "
            f"Retour prévu : {emprunt['date_retour_prevue']}"
        )


def lancer_console():
    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()

        try:
            if choix == "1":
                rechercher()
            elif choix == "2":
                emprunter()
            elif choix == "3":
                rendre()
            elif choix == "4":
                afficher_retards()
            elif choix == "0":
                print("Au revoir Et bonne lecture !")
                break
            else:
                print("Choix invalide. Réessayez.")

        except Exception as erreur:
            print(f"Une erreur est survenue : {erreur}")