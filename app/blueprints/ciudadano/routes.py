from flask import Blueprint
from flask import render_template
from flask import abort

from flask_login import login_required
from flask_login import current_user

from app.models.reporte import Reporte

ciudadano_bp = Blueprint(
    "ciudadano",
    __name__
)


@ciudadano_bp.route("/ciudadano")
@login_required
def dashboard():

    if current_user.id_rol != 2:
        abort(403)

    reportes = Reporte.query.filter_by(
        id_usuario=current_user.id_usuario
    ).order_by(
        Reporte.fecha_reporte.desc()
    ).all()

    total_reportes = len(reportes)

    pendientes = total_reportes

    return render_template(
        "ciudadano/dashboard.html",
        reportes=reportes,
        total_reportes=total_reportes,
        pendientes=pendientes
    )