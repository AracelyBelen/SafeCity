from app.extensions import db

class Zona(db.Model):

    __tablename__ = "zonas"

    id_zona = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre_zona = db.Column(
        db.String(100),
        nullable=False
    )

    distrito = db.Column(
        db.String(100)
    )

    descripcion = db.Column(
        db.String(200)
    )