# routes/public.py
# Module responsable des routes publiques du CMS (accueil, article, recherche).

from flask import Blueprint, render_template, request, abort
from models import article as article_model

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def accueil():
    """Affiche la page d'accueil avec les 5 derniers articles publiés."""
    articles = article_model.obtenir_articles_recents()
    return render_template("index.html", articles=articles)


@public_bp.route("/recherche")
def recherche():
    """Affiche les résultats de recherche pour un terme donné."""
    terme = request.args.get("q", "").strip()
    resultats = []
    if terme:
        resultats = article_model.rechercher_articles(terme)
    return render_template("recherche.html", resultats=resultats, terme=terme)


@public_bp.route("/article/<identifiant>")
def voir_article(identifiant):
    """Affiche la page d'un article selon son identifiant."""
    art = article_model.obtenir_article_par_identifiant(identifiant)
    if art is None:
        abort(404)
    return render_template("article.html", article=art)
