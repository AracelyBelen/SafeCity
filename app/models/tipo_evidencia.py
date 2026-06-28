from app.extensions import db

class TipoEvidencia(db.Model):

    __tablename__ = "tipos_evidencia"

    id_tipo_evidencia = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(50),
        nullable=False
    )