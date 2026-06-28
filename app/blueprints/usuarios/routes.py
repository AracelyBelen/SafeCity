from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required

from datetime import datetime

from app.extensions import db
from app.extensions import bcrypt

from app.models.usuario import Usuario
from app.models.rol import Rol

usuarios_bp = Blueprint(
    "usuarios",
    __name__
)

@usuarios_bp.route("/usuarios")
@login_required
def listar():

    usuarios = Usuario.query.all()

    return render_template(
        "usuarios/listar.html",
        usuarios=usuarios
    )

@usuarios_bp.route(
    "/usuarios/crear",
    methods=["GET", "POST"]
)
@login_required
def crear():

    roles = Rol.query.all()

    if request.method == "POST":

        password_hash = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        usuario = Usuario(

            nombre=request.form["nombre"],

            apellido=request.form["apellido"],

            username=request.form["username"],

            email=request.form["email"],

            password=password_hash,

            estado=True,

            fecha_registro=datetime.now(),

            id_rol=request.form["id_rol"]

        )

        db.session.add(usuario)

        db.session.commit()

        flash(
            "Usuario creado correctamente",
            "success"
        )

        return redirect(
            url_for(
                "usuarios.listar"
            )
        )

    return render_template(
        "usuarios/crear.html",
        roles=roles
    )

@usuarios_bp.route(
    "/usuarios/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar(id):

    usuario = Usuario.query.get_or_404(id)

    roles = Rol.query.all()

    if request.method == "POST":

        usuario.nombre = request.form["nombre"]

        usuario.apellido = request.form["apellido"]

        usuario.username = request.form["username"]

        usuario.email = request.form["email"]

        usuario.id_rol = request.form["id_rol"]

        db.session.commit()

        flash(
            "Usuario actualizado",
            "success"
        )

        return redirect(
            url_for(
                "usuarios.listar"
            )
        )

    return render_template(
        "usuarios/editar.html",
        usuario=usuario,
        roles=roles
    )

@usuarios_bp.route(
    "/usuarios/eliminar/<int:id>"
)
@login_required
def eliminar(id):

    usuario = Usuario.query.get_or_404(id)

    db.session.delete(
        usuario
    )

    db.session.commit()

    flash(
        "Usuario eliminado",
        "warning"
    )

    return redirect(
        url_for(
            "usuarios.listar"
        )
    )