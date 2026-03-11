# CMS INF5190 — Système de gestion de contenu

> Projet académique réalisé dans le cadre du cours **INF5190 — Programmation web avancée** à l'UQAM (Hiver 2026).

Un CMS (Content Management System) simple permettant de gérer les articles d'un site web, avec un système d'authentification et une interface d'administration complète.

---

## Fonctionnalités

- Page d'accueil avec les 5 derniers articles publiés
- Moteur de recherche dans les titres et contenus (SQL `LIKE`)
- Publication planifiée des articles (date de publication future)
- Interface d'administration protégée par authentification
- Création et modification d'articles avec validation des formulaires
- Gestion des utilisateurs (ajout, modification, désactivation)
- Photo de profil pour les auteurs
- Page 404 personnalisée

---

## Technologies utilisées

| Couche | Technologies |
|---|---|
| Back-end | Python 3, Flask, SQLite |
| Front-end | HTML5, CSS3 |
| Templating | Jinja2 |
| Base de données | SQLite (via module `sqlite3`) |

---

## Installation et lancement

### Prérequis
- Python 3.x installé
- pip

### Étapes

**1. Cloner le dépôt**
```bash
git clone https://github.com/mkoda-bit/cms-inf5190.git
cd cms-inf5190
```

**2. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**3. Lancer l'application**
```bash
python app.py
```

**4. Ouvrir dans le navigateur**
```
http://127.0.0.1:5000
```

---

## Accès à l'administration

| Champ | Valeur |
|---|---|
| URL | `http://127.0.0.1:5000/admin` |
| Utilisateur | `prof` |
| Mot de passe | `secret1234` |

---

## Structure du projet

```
cms/
├── app.py                  # Application Flask principale
├── database.py             # Initialisation et helpers BD
├── requirements.txt        # Dépendances Python
├── static/
│   └── uploads/            # Photos de profil des utilisateurs
└── templates/
    ├── base.html           # Gabarit commun
    ├── index.html          # Page d'accueil
    ├── article.html        # Page d'un article
    ├── recherche.html      # Résultats de recherche
    ├── login.html          # Connexion admin
    ├── admin.html          # Tableau de bord
    ├── admin_nouveau.html  # Créer un article
    ├── admin_modifier.html # Modifier un article
    ├── utilisateurs.html   # Gestion des utilisateurs
    └── 404.html            # Page d'erreur
```

---

## Contexte académique

Ce projet a été développé individuellement dans le cadre du **TP1** du cours INF5190 à l'UQAM. L'objectif était de concevoir un CMS fonctionnel en respectant les standards du web et les bonnes pratiques Python (PEP8).

---

*Manuella Koda — UQAM, Hiver 2026*
