import os
from datetime import timedelta

class Config:

    SECRET_KEY = "safecity_secret_key"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "safecity.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "app/static/uploads"

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "mp4"
    }

    # Cerrar sesión automáticamente tras 3 minutos de inactividad
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)