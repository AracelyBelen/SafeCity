from flask import Flask
from flask import render_template
from flask import session

from datetime import timedelta

from config import Config

from app.models.usuario import Usuario
from app.blueprints.auth import auth_bp

from app.extensions import (
    db,
    migrate,
    login_manager,
    bcrypt
)


@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(
        int(user_id)
    )


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Duración máxima de la sesión sin actividad
    app.permanent_session_lifetime = timedelta(minutes=3)

    @app.before_request
    def refresh_session():

        session.permanent = True

        # Reinicia el contador solamente cuando el usuario navega
        session.modified = True

    app.config["UPLOAD_FOLDER"] = "app/static/uploads"

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.login_message = (
        "Debes iniciar sesión para acceder."
    )

    login_manager.login_message_category = "warning"

    bcrypt.init_app(app)

    from app.models.rol import Rol
    from app.models.usuario import Usuario
    from app.models.categoria import Categoria
    from app.models.tipo_evidencia import TipoEvidencia
    from app.models.zona import Zona
    from app.models.reporte import Reporte
    from app.models.evidencia import Evidencia
    from app.models.reporte_zona import ReporteZona

    from app.blueprints.public import public_bp
    from app.blueprints.ciudadano import ciudadano_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.categorias import categorias_bp
    from app.blueprints.usuarios import usuarios_bp
    from app.blueprints.zonas import zonas_bp
    from app.blueprints.reportes import reportes_bp
    from app.blueprints.estadisticas import estadisticas_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ciudadano_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(zonas_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(estadisticas_bp)

    @app.errorhandler(403)
    def error_403(error):

        return render_template(
            "errors/403.html"
        ), 403

    @app.after_request
    def add_header(response):

        response.headers["Cache-Control"] = (
            "no-cache, no-store, must-revalidate"
        )

        response.headers["Pragma"] = "no-cache"

        response.headers["Expires"] = "0"

        return response

    return app