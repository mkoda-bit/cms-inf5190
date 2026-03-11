-- schema.sql
-- Schéma de la base de données du CMS.

CREATE TABLE IF NOT EXISTS utilisateur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    courriel TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL,
    photo TEXT,
    actif INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS article (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    identifiant TEXT NOT NULL UNIQUE,
    auteur TEXT NOT NULL,
    date_publication TEXT NOT NULL,
    contenu TEXT NOT NULL,
    utilisateur_id INTEGER NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);
