# models/article.py
# Module responsable des opérations de base de données liées aux articles.

import re
from flask import g
import config
import sqlite3


def get_db():
    """Retourne la connexion à la base de données active."""
    if "db" not in g:
        g.db = sqlite3.connect(
            config.DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def obtenir_articles_recents():
    """Retourne les 5 derniers articles publiés jusqu'à aujourd'hui."""
    db = get_db()
    return db.execute(
        "SELECT * FROM article WHERE date_publication <= date('now')"
        " ORDER BY date_publication DESC LIMIT 5"
    ).fetchall()


def rechercher_articles(terme):
    """Recherche les articles dont le titre ou le contenu contient le terme."""
    db = get_db()
    like = f"%{terme}%"
    return db.execute(
        "SELECT titre, identifiant, date_publication FROM article"
        " WHERE titre LIKE ? OR contenu LIKE ?",
        (like, like)
    ).fetchall()


def obtenir_article_par_identifiant(identifiant):
    """Retourne un article selon son identifiant unique."""
    db = get_db()
    return db.execute(
        "SELECT a.*, u.photo FROM article a"
        " JOIN utilisateur u ON a.utilisateur_id = u.id"
        " WHERE a.identifiant = ?",
        (identifiant,)
    ).fetchone()


def obtenir_tous_les_articles():
    """Retourne tous les articles pour l'interface d'administration."""
    db = get_db()
    return db.execute(
        "SELECT * FROM article ORDER BY date_publication DESC"
    ).fetchall()


def obtenir_article_par_id(article_id):
    """Retourne un article selon son id numérique."""
    db = get_db()
    return db.execute(
        "SELECT * FROM article WHERE id = ?", (article_id,)
    ).fetchone()


def valider_article(titre, identifiant, auteur, date_pub, contenu):
    """Valide les champs d'un article. Retourne une liste d'erreurs."""
    erreurs = []
    if not titre or not titre.strip():
        erreurs.append("Le titre est obligatoire.")
    if not identifiant or not identifiant.strip():
        erreurs.append("L'identifiant est obligatoire.")
    elif not re.match(r'^[a-zA-Z0-9\-_]+$', identifiant):
        erreurs.append(
            "L'identifiant ne peut contenir que des lettres, chiffres, "
            "tirets et tirets de soulignement."
        )
    if not auteur or not auteur.strip():
        erreurs.append("L'auteur est obligatoire.")
    if not date_pub:
        erreurs.append("La date de publication est obligatoire.")
    if not contenu or not contenu.strip():
        erreurs.append("Le contenu est obligatoire.")
    return erreurs


def creer_article(titre, identifiant, auteur, date_pub, contenu, user_id):
    """Insère un nouvel article dans la base de données."""
    db = get_db()
    db.execute(
        "INSERT INTO article (titre, identifiant, auteur, date_publication,"
        " contenu, utilisateur_id) VALUES (?, ?, ?, ?, ?, ?)",
        (titre, identifiant, auteur, date_pub, contenu, user_id)
    )
    db.commit()


def modifier_article(article_id, titre, contenu):
    """Modifie le titre et le contenu d'un article existant."""
    db = get_db()
    db.execute(
        "UPDATE article SET titre = ?, contenu = ? WHERE id = ?",
        (titre, contenu, article_id)
    )
    db.commit()


def identifiant_existe(identifiant, exclure_id=None):
    """Vérifie si un identifiant est déjà utilisé."""
    db = get_db()
    if exclure_id:
        row = db.execute(
            "SELECT id FROM article WHERE identifiant = ? AND id != ?",
            (identifiant, exclure_id)
        ).fetchone()
    else:
        row = db.execute(
            "SELECT id FROM article WHERE identifiant = ?",
            (identifiant,)
        ).fetchone()
    return row is not None
