from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from sqlalchemy import or_

from app.extensions import db
from app.extensions import bcrypt

from app.models.usuario import Usuario
from app.models.rol import Rol

from datetime import datetime

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    
    if current_user.is_authenticated:

        if current_user.rol.nombre == "Administrador":

            return redirect(
                url_for("admin.dashboard")
            )

        return redirect(
            url_for("ciudadano.dashboard")
        )

    if request.method == "POST":

        login_value = request.form["login"].strip()

        password = request.form["password"]

        usuario = Usuario.query.filter(
            (Usuario.username == login_value) |
            (Usuario.email == login_value)
        ).first()

        if usuario and bcrypt.check_password_hash(
            usuario.password,
            password
        ):
            
            session.permanent=True
            login_user(usuario)

            if usuario.rol.nombre == "Administrador":

                return redirect(
                    url_for("admin.dashboard")
                )

            return redirect(
                url_for("ciudadano.dashboard")
            )

        flash(
            "Credenciales incorrectas",
            "danger"
        )

    return render_template(
        "auth/login.html"
    )


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():
    
    if current_user.is_authenticated:

        if current_user.rol.nombre == "Administrador":

            return redirect(
                url_for("admin.dashboard")
            )

        return redirect(
            url_for("ciudadano.dashboard")
        )

    if request.method == "POST":

        nombre = request.form["nombre"]

        apellido = request.form["apellido"]

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash(
                "Las contraseñas no coinciden",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        existe_usuario = Usuario.query.filter_by(
            username=username
        ).first()

        if existe_usuario:

            flash(
                "El usuario ya existe",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        existe_email = Usuario.query.filter_by(
            email=email
        ).first()

        if existe_email:

            flash(
                "El correo electrónico ya está registrado",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        rol_ciudadano = Rol.query.filter_by(
            nombre="Ciudadano"
        ).first()

        password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        nuevo_usuario = Usuario(

            nombre=nombre,

            apellido=apellido,

            username=username,

            email=email,

            password=password_hash,

            estado=True,

            fecha_registro=datetime.now(),

            id_rol=rol_ciudadano.id_rol

        )

        db.session.add(nuevo_usuario)

        db.session.commit()

        flash(
            "Registro exitoso",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    
    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("public.index")
    )