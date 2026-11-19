from dataclasses import dataclass
from typing import Optional


@dataclass
class Livre:
    id: Optional[int]
    code: str
    titre: str
    auteur: str
    categorie: str
    annee_publication: Optional[int]
    quantite_totale: int
    quantite_disponible: int


@dataclass
class Lecteur:
    id: Optional[int]
    matricule: str
    nom: str
    prenom: str


@dataclass
class Emprunt:
    id: Optional[int]
    livre_id: int
    lecteur_id: int
    date_emprunt: str
    date_retour_prevue: str
    date_retour_effective: Optional[str]