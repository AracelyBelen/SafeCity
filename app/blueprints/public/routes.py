from flask import Blueprint
from flask import render_template
from flask import jsonify

from sqlalchemy import func

from app.extensions import db

from app.models.reporte import Reporte
from app.models.usuario import Usuario
from app.models.zona import Zona
from app.models.reporte_zona import ReporteZona

public_bp = Blueprint(
    "public",
    __name__
)


@public_bp.route("/")
def index():

    reportes = Reporte.query.order_by(
        Reporte.fecha_reporte.desc()
    ).all()

    marcadores = []

    for reporte in reportes:

        if (
            reporte.latitud is not None
            and
            reporte.longitud is not None
        ):

            marcadores.append({

                "titulo": reporte.titulo,

                "descripcion": reporte.descripcion,

                "latitud": reporte.latitud,

                "longitud": reporte.longitud

            })

    total_reportes = Reporte.query.count()

    usuarios_activos = Usuario.query.filter_by(
        estado=True
    ).count()

    return render_template(

        "public/index.html",

        reportes=reportes,

        marcadores=marcadores,

        total_reportes=total_reportes,

        usuarios_activos=usuarios_activos

    )


@public_bp.route("/api/estadisticas")
def api_estadisticas():

    total_reportes = Reporte.query.count()

    usuarios_activos = Usuario.query.filter_by(
        estado=True
    ).count()

    return jsonify({

        "reportes": total_reportes,

        "usuarios": usuarios_activos

    })


@public_bp.route("/api/ultimos-reportes")
def api_ultimos_reportes():

    reportes = Reporte.query.order_by(
        Reporte.fecha_reporte.desc()
    ).limit(5).all()

    datos = []

    for reporte in reportes:

        categoria = "Sin categoría"

        if reporte.categoria:

            categoria = reporte.categoria.nombre

        descripcion = reporte.descripcion or ""

        if len(descripcion) > 80:

            descripcion = descripcion[:80] + "..."

        imagen = None

        if reporte.evidencias:

            evidencia = reporte.evidencias[0]

            if evidencia.id_tipo_evidencia == 1:

                imagen = f"/static/uploads/{evidencia.archivo}"

        datos.append({

            "categoria": categoria,

            "descripcion": descripcion,

            "fecha": reporte.fecha_reporte.strftime(
                "%d/%m/%Y %H:%M"
            ),

            "imagen": imagen

        })

    return jsonify(datos)


@public_bp.route("/api/top-zonas")
def api_top_zonas():

    resultados = db.session.query(

        Zona.nombre_zona,

        func.count(
            ReporteZona.id_reporte
        ).label("total")

    ).join(

        ReporteZona,

        Zona.id_zona == ReporteZona.id_zona

    ).group_by(

        Zona.id_zona,

        Zona.nombre_zona

    ).order_by(

        func.count(
            ReporteZona.id_reporte
        ).desc()

    ).limit(5).all()

    datos = []

    for zona, total in resultados:

        datos.append({

            "zona": zona,

            "total": total

        })

    return jsonify(datos)


@public_bp.route("/mapa")
def mapa():

    reportes = Reporte.query.filter(
        Reporte.latitud.isnot(None),
        Reporte.longitud.isnot(None)
    ).all()

    marcadores = []

    for reporte in reportes:

        marcadores.append({

            "titulo": reporte.titulo,

            "descripcion": reporte.descripcion,

            "latitud": reporte.latitud,

            "longitud": reporte.longitud

        })

    return render_template(

        "public/mapa.html",

        marcadores=marcadores

    )