from app.extensions import db

class Evidencia(db.Model):

    __tablename__ = "evidencias"

    id_evidencia = db.Column(
        db.Integer,
        primary_key=True
    )

    archivo = db.Column(
        db.String(255),
        nullable=False
    )

    fecha_subida = db.Column(
        db.DateTime
    )

    id_reporte = db.Column(
        db.Integer,
        db.ForeignKey(
            "reportes.id_reporte"
        )
    )

    id_tipo_evidencia = db.Column(
        db.Integer,
        db.ForeignKey(
            "tipos_evidencia.id_tipo_evidencia"
        )
    )