# routes/admin.py
# Module responsable des routes d'administration du CMS
# (authentification, gestion des articles).

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)
from models import article as article_model
from models import utilisateur as user_model

admin_bp = Blueprint("admin", __name__)


def exiger_authentification():
    """Redirige vers la page de connexion si l'utilisateur n'est pas connecté."""
    if "user_id" not in session:
        return redirect(url_for("admin.connexion"))
    return None


@admin_bp.route("/admin", methods=["GET", "POST"])
def connexion():
    """Affiche le formulaire de connexion et authentifie l'utilisateur."""
    if "user_id" in session:
        return redirect(url_for("admin.tableau_de_bord"))

    erreur = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        mot_de_passe = request.form.get("mot_de_passe", "")
        utilisateur = user_model.authentifier(username, mot_de_passe)
        if utilisateur:
            session["user_id"] = utilisateur["id"]
            session["username"] = utilisateur["username"]
            return redirect(url_for("admin.tableau_de_bord"))
        erreur = "Nom d'utilisateur ou mot de passe incorrect."

    return render_template("admin/login.html", erreur=erreur)


@admin_bp.route("/admin/tableau-de-bord")
def tableau_de_bord():
    """Affiche la liste des articles pour l'administrateur connecté."""
    redirection = exiger_authentification()
    if redirection:
        return redirection
    articles = article_model.obtenir_tous_les_articles()
    return render_template("admin/dashboard.html", articles=articles)


@admin_bp.route("/admin/deconnexion")
def deconnexion():
    """Déconnecte l'utilisateur et redirige vers la page de connexion."""
    session.clear()
    return redirect(url_for("admin.connexion"))


@admin_bp.route("/admin-nouveau", methods=["GET"])
def nouveau_article_form():
    """Affiche le formulaire de création d'un nouvel article."""
    redirection = exiger_authentification()
    if redirection:
        return redirection
    return render_template("admin/nouveau.html", erreurs=[], valeurs={})


@admin_bp.route("/admin-nouveau", methods=["POST"])
def creer_article():
    """Traite la soumission du formulaire de création d'article."""
    redirection = exiger_authentification()
    if redirection:
        return redirection

    titre = request.form.get("titre", "").strip()
    identifiant = request.form.get("identifiant", "").strip()
    auteur = request.form.get("auteur", "").strip()
    date_pub = request.form.get("date_publication", "").strip()
    contenu = request.form.get("contenu", "").strip()

    erreurs = article_model.valider_article(
        titre, identifiant, auteur, date_pub, contenu
    )

    if not erreurs and article_model.identifiant_existe(identifiant):
        erreurs.append("Cet identifiant est déjà utilisé.")

    if erreurs:
        valeurs = {
            "titre": titre,
            "identifiant": identifiant,
            "auteur": auteur,
            "date_publication": date_pub,
            "contenu": contenu
        }
        return render_template(
            "admin/nouveau.html", erreurs=erreurs, valeurs=valeurs
        ), 422

    article_model.creer_article(
        titre, identifiant, auteur, date_pub, contenu, session["user_id"]
    )
    flash("Article créé avec succès.", "succes")
    return redirect(url_for("admin.tableau_de_bord"))


@admin_bp.route("/admin/modifier/<int:article_id>", methods=["GET"])
def modifier_article_form(article_id):
    """Affiche le formulaire de modification d'un article."""
    redirection = exiger_authentification()
    if redirection:
        return redirection
    art = article_model.obtenir_article_par_id(article_id)
    if art is None:
        return render_template("404.html"), 404
    return render_template("admin/modifier.html", article=art, erreurs=[])


@admin_bp.route("/admin/modifier/<int:article_id>", methods=["POST"])
def modifier_article(article_id):
    """Traite la soumission du formulaire de modification d'article."""
    redirection = exiger_authentification()
    if redirection:
        return redirection

    art = article_model.obtenir_article_par_id(article_id)
    if art is None:
        return render_template("404.html"), 404

    titre = request.form.get("titre", "").strip()
    contenu = request.form.get("contenu", "").strip()

    erreurs = []
    if not titre:
        erreurs.append("Le titre est obligatoire.")
    if not contenu:
        erreurs.append("Le contenu est obligatoire.")

    if erreurs:
        return render_template(
            "admin/modifier.html", article=art, erreurs=erreurs
        ), 422

    article_model.modifier_article(article_id, titre, contenu)
    flash("Article modifié avec succès.", "succes")
    return redirect(url_for("admin.tableau_de_bord"))
