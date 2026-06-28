from flask import Blueprint
from flask import render_template
from flask_login import current_user
from flask_login import login_required

from app.models.usuario import Usuario
from app.models.reporte import Reporte
from app.models.categoria import Categoria
from app.models.zona import Zona
from flask import abort

from flask import redirect
from flask import url_for
from flask import flash

from app.extensions import db
admin_bp = Blueprint(
    "admin",
    __name__
)

@admin_bp.route("/admin")
@login_required
def dashboard():
    if current_user.id_rol != 1:
        abort(403)
        
    total_usuarios = Usuario.query.count()

    total_reportes = Reporte.query.count()

    total_categorias = Categoria.query.count()

    total_zonas = Zona.query.count()

    return render_template(
        "admin/dashboard.html",

        total_usuarios=total_usuarios,

        total_reportes=total_reportes,

        total_categorias=total_categorias,

        total_zonas=total_zonas
    )
    
@admin_bp.route("/admin/reportes")
@login_required
def reportes():

    todos_los_reportes = Reporte.query.order_by(
        Reporte.fecha_reporte.desc()
    ).all()

    return render_template(
        "admin/reportes.html",
        reportes=todos_los_reportes
    )
    
@admin_bp.route("/admin/reportes/eliminar/<int:id>")
@login_required
def eliminar_reporte(id):

    if current_user.id_rol != 1:
        abort(403)

    reporte = Reporte.query.get_or_404(id)

    db.session.delete(reporte)

    db.session.commit()

    flash(
        "Reporte eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for("admin.reportes")
    )