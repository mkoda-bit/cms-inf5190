import os
import sqlite3
from flask import Flask, render_template, g
import config
from routes.public import public_bp
from routes.admin import admin_bp
from routes.utilisateurs import utilisateurs_bp


def creer_application():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
    app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(utilisateurs_bp)

    app.teardown_appcontext(fermer_db)
    app.register_error_handler(404, gerer_404)
    app.register_error_handler(500, gerer_500)

    return app


def fermer_db(e=None):
    """Ferme la connexion à la base de données en fin de requête."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def gerer_404(e):
    """Retourne la page d'erreur 404."""
    return render_template("404.html"), 404


def gerer_500(e):
    """Retourne la page d'erreur 500."""
    return render_template("500.html"), 500


def initialiser_base_de_donnees(app):
    """Crée les tables et l'utilisateur par défaut si nécessaire."""
    with app.app_context():
        db = sqlite3.connect(config.DATABASE)
        db.row_factory = sqlite3.Row
        with app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf8"))

        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
        inserer_utilisateur_prof(db)
        db.close()


def inserer_utilisateur_prof(db):
    """Insère l'utilisateur 'prof' s'il n'existe pas déjà."""
    import hashlib
    existant = db.execute(
        "SELECT id FROM utilisateur WHERE username = 'prof'"
    ).fetchone()
    if existant is None:
        hache = hashlib.sha256("secret1234".encode("utf-8")).hexdigest()
        db.execute(
            "INSERT INTO utilisateur (nom, prenom, courriel, username,"
            " mot_de_passe, actif) VALUES (?, ?, ?, ?, ?, 1)",
            ("Professeur", "Test", "prof@example.com", "prof", hache)
        )
        db.commit()


app = creer_application()

if __name__ == "__main__":
    initialiser_base_de_donnees(app)
    app.run(debug=True)
