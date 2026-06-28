from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from datetime import datetime

from app.extensions import db
from app.models.evidencia import Evidencia
from app.models.reporte import Reporte
from app.models.reporte_zona import ReporteZona
from app.models.categoria import Categoria
from app.models.zona import Zona

from werkzeug.utils import secure_filename

import os
ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "mp4"
}

def archivo_permitido(nombre_archivo):

    return (
        "." in nombre_archivo
        and
        nombre_archivo.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS)


reportes_bp = Blueprint(
    "reportes",
    __name__
)


@reportes_bp.route("/reportes")
@login_required
def listar():

    reportes = Reporte.query.filter_by(
        id_usuario=current_user.id_usuario
    ).all()

    return render_template(
        "reportes/listar.html",
        reportes=reportes
    )


@reportes_bp.route(
    "/reportes/crear",
    methods=["GET", "POST"]
)
@login_required
def crear():

    categorias = Categoria.query.all()
    zonas = Zona.query.all()

    if request.method == "POST":

        imagenes = request.files.getlist(
            "evidencia_imagen"
        )

        video = request.files.get(
            "evidencia_video"
        )

        imagenes_validas = [

            imagen for imagen in imagenes

            if imagen and imagen.filename != ""

        ]

        hay_video = video and video.filename != ""

        if len(imagenes_validas) > 5:

            flash(
                "Solo puedes subir un máximo de 5 imágenes.",
                "danger"
            )

            return redirect(
                url_for("reportes.crear")
            )

        if len(imagenes_validas) > 1 and hay_video:

            flash(
                "Solo puedes adjuntar un video junto con una única imagen.",
                "danger"
            )

            return redirect(
                url_for("reportes.crear")
            )

        if len(imagenes_validas) == 0 and not hay_video:

            flash(
                "Debes adjuntar al menos una imagen o un video.",
                "danger"
            )

            return redirect(
                url_for("reportes.crear")
            )

        for imagen in imagenes_validas:

            extension = imagen.filename.rsplit(
                ".",
                1
            )[1].lower()

            if extension not in [
                "jpg",
                "jpeg",
                "png"
            ]:

                flash(
                    "Solo se permiten imágenes JPG o PNG.",
                    "danger"
                )

                return redirect(
                    url_for("reportes.crear")
                )

        if hay_video:

            extension = video.filename.rsplit(
                ".",
                1
            )[1].lower()

            if extension != "mp4":

                flash(
                    "Solo se permiten videos MP4.",
                    "danger"
                )

                return redirect(
                    url_for("reportes.crear")
                )

        latitud = request.form.get(
            "latitud"
        )

        longitud = request.form.get(
            "longitud"
        )

        reporte = Reporte(

            titulo=request.form.get(
                "titulo",
                "Reporte ciudadano"
            ),

            descripcion=request.form[
                "descripcion"
            ],

            fecha_reporte=datetime.now(),

            latitud=float(latitud)
            if latitud else None,

            longitud=float(longitud)
            if longitud else None,

            id_usuario=current_user.id_usuario,

            id_categoria=request.form[
                "id_categoria"
            ]

        )

        db.session.add(reporte)

        db.session.commit()

        for imagen in imagenes_validas:

            nombre_archivo = secure_filename(
                imagen.filename
            )

            ruta = os.path.join(
                "app",
                "static",
                "uploads",
                nombre_archivo
            )

            imagen.save(ruta)

            evidencia = Evidencia(

                archivo=nombre_archivo,

                fecha_subida=datetime.now(),

                id_reporte=reporte.id_reporte,

                id_tipo_evidencia=1

            )

            db.session.add(evidencia)

        if hay_video:

            nombre_video = secure_filename(
                video.filename
            )

            ruta = os.path.join(
                "app",
                "static",
                "uploads",
                nombre_video
            )

            video.save(ruta)

            evidencia = Evidencia(

                archivo=nombre_video,

                fecha_subida=datetime.now(),

                id_reporte=reporte.id_reporte,

                id_tipo_evidencia=2

            )

            db.session.add(evidencia)

        reporte_zona = ReporteZona(

            id_reporte=reporte.id_reporte,

            id_zona=request.form[
                "id_zona"
            ]

        )

        db.session.add(reporte_zona)

        db.session.commit()

        flash(
            "Reporte creado correctamente.",
            "success"
        )

        return redirect(
            url_for(
                "ciudadano.dashboard"
            )
        )

    return render_template(
        "reportes/crear.html",
        categorias=categorias,
        zonas=zonas
    )


@reportes_bp.route(
    "/reportes/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar(id):

    reporte = Reporte.query.get_or_404(
        id
    )
    if reporte.id_usuario != current_user.id_usuario:
        flash(
            "No tienes permiso para editar este reporte.",
            "danger"
        )
        return redirect(
            url_for("ciudadano.dashboard")
        )
    categorias = Categoria.query.all()

    zonas = Zona.query.all()

    if request.method == "POST":

        reporte.descripcion = request.form[
            "descripcion"
        ]

        reporte.id_categoria = request.form[
            "id_categoria"
        ]
        
        reporte.fecha_actualizacion = datetime.now()
        latitud = request.form.get("latitud")
        longitud = request.form.get("longitud")
        reporte.latitud = float(latitud) if latitud else None
        reporte.longitud = float(longitud) if longitud else None
        reporte_zona = ReporteZona.query.filter_by(
            id_reporte=reporte.id_reporte
        ).first()

        if reporte_zona:

            reporte_zona.id_zona = request.form[
                "id_zona"
            ]

        db.session.commit()

        flash(
            "Reporte actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for(
                "ciudadano.dashboard"
            )
        )

    return render_template(
        "reportes/editar.html",
        reporte=reporte,
        categorias=categorias,
        zonas=zonas
    )


@reportes_bp.route(
    "/reportes/eliminar/<int:id>"
)
@login_required
def eliminar(id):

    reporte = Reporte.query.get_or_404(
        id
    )
    if reporte.id_usuario != current_user.id_usuario:
        flash(
            "No tienes permiso para eliminar este reporte.",
            "danger"
        )
        return redirect(
            url_for("ciudadano.dashboard")
        )
    evidencia = Evidencia.query.filter_by(
        id_reporte=id
    ).all()

    for item in evidencia:

        ruta = os.path.join(
            "app",
            "static",
            "uploads",
            item.archivo
        )

        if os.path.exists(ruta):

            os.remove(ruta)

        db.session.delete(item)

    reporte_zona = ReporteZona.query.filter_by(
        id_reporte=id
    ).first()

    if reporte_zona:

        db.session.delete(
            reporte_zona
        )

    db.session.delete(
        reporte
    )

    db.session.commit()

    flash(
        "Reporte eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for(
              "ciudadano.dashboard"
        )
    )