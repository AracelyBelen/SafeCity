from flask import Blueprint
from flask import render_template

from app.models.reporte import Reporte
from app.models.categoria import Categoria
from app.models.zona import Zona
from app.models.usuario import Usuario

estadisticas_bp = Blueprint(
    "estadisticas",
    __name__
)


@estadisticas_bp.route("/estadisticas")
def estadisticas():

    total_reportes = Reporte.query.count()

    total_categorias = Categoria.query.count()

    total_zonas = Zona.query.count()

    usuarios_activos = Usuario.query.filter_by(
        estado=True
    ).count()

    return render_template(

        "public/estadisticas.html",

        total_reportes=total_reportes,

        total_categorias=total_categorias,

        total_zonas=total_zonas,

        usuarios_activos=usuarios_activos

    )