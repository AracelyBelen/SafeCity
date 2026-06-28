from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required

from app.extensions import db

from app.models.categoria import Categoria

categorias_bp = Blueprint(
    "categorias",
    __name__
)

@categorias_bp.route("/categorias")
@login_required
def listar():

    categorias = Categoria.query.all()

    return render_template(
        "categorias/listar.html",
        categorias=categorias
    )

@categorias_bp.route(
    "/categorias/crear",
    methods=["GET", "POST"]
)
@login_required
def crear():

    if request.method == "POST":

        nombre = request.form["nombre"]

        descripcion = request.form["descripcion"]

        categoria = Categoria(

            nombre=nombre,

            descripcion=descripcion

        )

        db.session.add(
            categoria
        )

        db.session.commit()

        flash(
            "Categoría creada",
            "success"
        )

        return redirect(
            url_for(
                "categorias.listar"
            )
        )

    return render_template(
        "categorias/crear.html"
    )

@categorias_bp.route(
    "/categorias/editar/<int:id>"
    ,
    methods=["GET", "POST"]
)
@login_required
def editar(id):

    categoria = Categoria.query.get_or_404(id)

    if request.method == "POST":

        categoria.nombre = request.form["nombre"]

        categoria.descripcion = request.form["descripcion"]

        db.session.commit()

        flash(
            "Categoría actualizada",
            "success"
        )

        return redirect(
            url_for(
                "categorias.listar"
            )
        )

    return render_template(
        "categorias/editar.html",
        categoria=categoria
    )

@categorias_bp.route(
    "/categorias/eliminar/<int:id>"
)
@login_required
def eliminar(id):

    categoria = Categoria.query.get_or_404(id)

    db.session.delete(
        categoria
    )

    db.session.commit()

    flash(
        "Categoría eliminada",
        "warning"
    )

    return redirect(
        url_for(
            "categorias.listar"
        )
    )

