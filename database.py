
import sqlite3
import os
from flask import g
import config


def get_db(app):
    """Retourne la connexion à la base de données pour la requête courante."""
    if "db" not in g:
        g.db = sqlite3.connect(
            config.DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(app, e=None):
    """Ferme la connexion à la base de données si elle est ouverte."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db(app)
        with app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf8"))
        db.commit()


def create_upload_folder():
    """Crée le dossier d'upload s'il n'existe pas."""
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
