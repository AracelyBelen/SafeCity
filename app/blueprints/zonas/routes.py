from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required

from app.extensions import db

from app.models.zona import Zona

zonas_bp = Blueprint(
    "zonas",
    __name__
)

@zonas_bp.route("/zonas")
@login_required
def listar():

    zonas = Zona.query.all()

    return render_template(
        "zonas/listar.html",
        zonas=zonas
    )

@zonas_bp.route(
    "/zonas/crear",
    methods=["GET", "POST"]
)
@login_required
def crear():

    if request.method == "POST":

        zona = Zona(

            nombre_zona=request.form["nombre_zona"],

            distrito=request.form["distrito"],

            descripcion=request.form["descripcion"]

        )

        db.session.add(zona)

        db.session.commit()

        flash(
            "Zona creada correctamente",
            "success"
        )

        return redirect(
            url_for(
                "zonas.listar"
            )
        )

    return render_template(
        "zonas/crear.html"
    )

@zonas_bp.route(
    "/zonas/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar(id):

    zona = Zona.query.get_or_404(id)

    if request.method == "POST":

        zona.nombre_zona = request.form["nombre_zona"]

        zona.distrito = request.form["distrito"]

        zona.descripcion = request.form["descripcion"]

        db.session.commit()

        flash(
            "Zona actualizada",
            "success"
        )

        return redirect(
            url_for(
                "zonas.listar"
            )
        )

    return render_template(
        "zonas/editar.html",
        zona=zona
    )

@zonas_bp.route(
    "/zonas/eliminar/<int:id>"
)
@login_required
def eliminar(id):

    zona = Zona.query.get_or_404(id)

    db.session.delete(zona)

    db.session.commit()

    flash(
        "Zona eliminada",
        "warning"
    )

    return redirect(
        url_for(
            "zonas.listar"
        )
    )

