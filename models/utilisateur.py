# models/utilisateur.py
# Module responsable des opérations de base de données liées aux utilisateurs.

import hashlib
import os
import sqlite3
from flask import g
import config


def get_db():
    """Retourne la connexion à la base de données active."""
    if "db" not in g:
        g.db = sqlite3.connect(
            config.DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def hacher_mot_de_passe(mot_de_passe):
    """Retourne le hachage SHA-256 du mot de passe."""
    return hashlib.sha256(mot_de_passe.encode("utf-8")).hexdigest()


def authentifier(username, mot_de_passe):
    """Retourne l'utilisateur si les identifiants sont valides, sinon None."""
    db = get_db()
    hache = hacher_mot_de_passe(mot_de_passe)
    return db.execute(
        "SELECT * FROM utilisateur WHERE username = ? AND mot_de_passe = ?"
        " AND actif = 1",
        (username, hache)
    ).fetchone()


def obtenir_tous_les_utilisateurs():
    """Retourne la liste de tous les utilisateurs."""
    db = get_db()
    return db.execute(
        "SELECT * FROM utilisateur ORDER BY nom, prenom"
    ).fetchall()


def obtenir_utilisateur_par_id(user_id):
    """Retourne un utilisateur selon son identifiant numérique."""
    db = get_db()
    return db.execute(
        "SELECT * FROM utilisateur WHERE id = ?", (user_id,)
    ).fetchone()


def valider_utilisateur(nom, prenom, courriel, username, mot_de_passe):
    """Valide les champs d'un utilisateur. Retourne une liste d'erreurs."""
    erreurs = []
    if not nom or not nom.strip():
        erreurs.append("Le nom est obligatoire.")
    if not prenom or not prenom.strip():
        erreurs.append("Le prénom est obligatoire.")
    if not courriel or "@" not in courriel:
        erreurs.append("Le courriel est invalide.")
    if not username or not username.strip():
        erreurs.append("Le nom d'utilisateur est obligatoire.")
    if not mot_de_passe or len(mot_de_passe) < 6:
        erreurs.append("Le mot de passe doit contenir au moins 6 caractères.")
    return erreurs


def creer_utilisateur(nom, prenom, courriel, username, mot_de_passe, photo):
    """Insère un nouvel utilisateur dans la base de données."""
    db = get_db()
    hache = hacher_mot_de_passe(mot_de_passe)
    db.execute(
        "INSERT INTO utilisateur (nom, prenom, courriel, username,"
        " mot_de_passe, photo) VALUES (?, ?, ?, ?, ?, ?)",
        (nom, prenom, courriel, username, hache, photo)
    )
    db.commit()


def modifier_utilisateur(user_id, nom, prenom, courriel, photo):
    """Modifie les informations d'un utilisateur existant."""
    db = get_db()
    db.execute(
        "UPDATE utilisateur SET nom = ?, prenom = ?, courriel = ?,"
        " photo = ? WHERE id = ?",
        (nom, prenom, courriel, photo, user_id)
    )
    db.commit()


def modifier_mot_de_passe(user_id, mot_de_passe):
    """Modifie le mot de passe d'un utilisateur."""
    db = get_db()
    hache = hacher_mot_de_passe(mot_de_passe)
    db.execute(
        "UPDATE utilisateur SET mot_de_passe = ? WHERE id = ?",
        (hache, user_id)
    )
    db.commit()


def basculer_statut(user_id):
    """Active ou désactive un utilisateur."""
    db = get_db()
    db.execute(
        "UPDATE utilisateur SET actif = CASE WHEN actif = 1 THEN 0 ELSE 1 END"
        " WHERE id = ?",
        (user_id,)
    )
    db.commit()


def sauvegarder_photo(fichier):
    """Sauvegarde la photo de profil et retourne son nom de fichier."""
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    ext = fichier.filename.rsplit(".", 1)[-1].lower()
    nom_fichier = f"{os.urandom(8).hex()}.{ext}"
    chemin = os.path.join(config.UPLOAD_FOLDER, nom_fichier)
    fichier.save(chemin)
    return nom_fichier


def username_existe(username, exclure_id=None):
    """Vérifie si un nom d'utilisateur est déjà pris."""
    db = get_db()
    if exclure_id:
        row = db.execute(
            "SELECT id FROM utilisateur WHERE username = ? AND id != ?",
            (username, exclure_id)
        ).fetchone()
    else:
        row = db.execute(
            "SELECT id FROM utilisateur WHERE username = ?",
            (username,)
        ).fetchone()
    return row is not None
