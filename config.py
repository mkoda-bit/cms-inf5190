# config.py
# Fichier de configuration du CMS.
#
# Structure:
#   SECRET_KEY        : Clé secrète Flask pour les sessions (changer en production)
#   DATABASE          : Chemin vers le fichier SQLite
#   UPLOAD_FOLDER     : Dossier pour les photos de profil
#   MAX_CONTENT_LENGTH: Taille maximale des fichiers uploadés (en octets)

SECRET_KEY = "changez-moi-en-production"
DATABASE = "cms.db"
UPLOAD_FOLDER = "static/uploads"
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 Mo
