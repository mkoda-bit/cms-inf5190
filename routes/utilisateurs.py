# routes/utilisateurs.py
# Module responsable des routes de gestion des utilisateurs du CMS.

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)
from models import utilisateur as user_model

utilisateurs_bp = Blueprint("utilisateurs", __name__)

EXTENSIONS_PERMISES = {"png", "jpg", "jpeg", "gif", "webp"}


def exiger_authentification():
    """Redirige vers la page de connexion si l'utilisateur n'est pas connecté."""
    if "user_id" not in session:
        return redirect(url_for("admin.connexion"))
    return None


def extension_permise(nom_fichier):
    """Vérifie si l'extension du fichier est autorisée."""
    return (
        "." in nom_fichier
        and nom_fichier.rsplit(".", 1)[1].lower() in EXTENSIONS_PERMISES
    )


@utilisateurs_bp.route("/utilisateurs")
def liste_utilisateurs():
    """Affiche la liste des utilisateurs pour l'administrateur."""
    redirection = exiger_authentification()
    if redirection:
        return redirection
    utilisateurs = user_model.obtenir_tous_les_utilisateurs()
    return render_template(
        "utilisateurs/index.html", utilisateurs=utilisateurs
    )


@utilisateurs_bp.route("/utilisateurs/nouveau", methods=["GET"])
def nouveau_utilisateur_form():
    """Affiche le formulaire d'ajout d'un utilisateur."""
    redirection = exiger_authentification()
    if redirection:
        return redirection
    return render_template(
        "utilisateurs/nouveau.html", erreurs=[], valeurs={}
    )


@utilisateurs_bp.route("/utilisateurs/nouveau", methods=["POST"])
def creer_utilisateur():
    """Traite la création d'un nouvel utilisateur."""
    redirection = exiger_authentification()
    if redirection:
        return redirection

    nom = request.form.get("nom", "").strip()
    prenom = request.form.get("prenom", "").strip()
    courriel = request.form.get("courriel", "").strip()
    username = request.form.get("username", "").strip()
    mot_de_passe = request.form.get("mot_de_passe", "")
    fichier = request.files.get("photo")

    erreurs = user_model.valider_utilisateur(
        nom, prenom, courriel, username, mot_de_passe
    )

    if not erreurs and user_model.username_existe(username):
        erreurs.append("Ce nom d'utilisateur est déjà pris.")

    photo = None
    if fichier and fichier.filename:
        if not extension_permise(fichier.filename):
            erreurs.append(
                "Format de photo invalide (png, jpg, jpeg, gif, webp)."
            )
        else:
            photo = user_model.sauvegarder_photo(fichier)

    if erreurs:
        valeurs = {
            "nom": nom, "prenom": prenom,
            "courriel": courriel, "username": username
        }
        return render_template(
            "utilisateurs/nouveau.html", erreurs=erreurs, valeurs=valeurs
        ), 422

    user_model.creer_utilisateur(
        nom, prenom, courriel, username, mot_de_passe, photo
    )
    flash("Utilisateur créé avec succès.", "succes")
    return redirect(url_for("utilisateurs.liste_utilisateurs"))


@utilisateurs_bp.route(
    "/utilisateurs/modifier/<int:user_id>", methods=["GET"]
)
def modifier_utilisateur_form(user_id):
    """Affiche le formulaire de modification d'un utilisateur."""
    redirection = exiger_authentification()
    if redirection:
        return redirection
    utilisateur = user_model.obtenir_utilisateur_par_id(user_id)
    if utilisateur is None:
        return render_template("404.html"), 404
    return render_template(
        "utilisateurs/modifier.html", utilisateur=utilisateur, erreurs=[]
    )


@utilisateurs_bp.route(
    "/utilisateurs/modifier/<int:user_id>", methods=["POST"]
)
def modifier_utilisateur(user_id):
    """Traite la modification d'un utilisateur existant."""
    redirection = exiger_authentification()
    if redirection:
        return redirection

    utilisateur = user_model.obtenir_utilisateur_par_id(user_id)
    if utilisateur is None:
        return render_template("404.html"), 404

    nom = request.form.get("nom", "").strip()
    prenom = request.form.get("prenom", "").strip()
    courriel = request.form.get("courriel", "").strip()
    fichier = request.files.get("photo")
    mot_de_passe = request.form.get("mot_de_passe", "")

    erreurs = []
    if not nom:
        erreurs.append("Le nom est obligatoire.")
    if not prenom:
        erreurs.append("Le prénom est obligatoire.")
    if not courriel or "@" not in courriel:
        erreurs.append("Le courriel est invalide.")

    photo = utilisateur["photo"]
    if fichier and fichier.filename:
        if not extension_permise(fichier.filename):
            erreurs.append(
                "Format de photo invalide (png, jpg, jpeg, gif, webp)."
            )
        else:
            photo = user_model.sauvegarder_photo(fichier)

    if erreurs:
        return render_template(
            "utilisateurs/modifier.html",
            utilisateur=utilisateur, erreurs=erreurs
        ), 422

    user_model.modifier_utilisateur(user_id, nom, prenom, courriel, photo)
    if mot_de_passe:
        user_model.modifier_mot_de_passe(user_id, mot_de_passe)
    flash("Utilisateur modifié avec succès.", "succes")
    return redirect(url_for("utilisateurs.liste_utilisateurs"))


@utilisateurs_bp.route(
    "/utilisateurs/statut/<int:user_id>", methods=["POST"]
)
def basculer_statut(user_id):
    """Active ou désactive un utilisateur."""
    redirection = exiger_authentification()
    if redirection:
        return redirection
    user_model.basculer_statut(user_id)
    flash("Statut de l'utilisateur modifié.", "succes")
    return redirect(url_for("utilisateurs.liste_utilisateurs"))
