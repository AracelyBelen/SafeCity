from app.extensions import db

class Rol(db.Model):

    __tablename__ = "roles"

    id_rol = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    descripcion = db.Column(
        db.String(200)
    )

    usuarios = db.relationship(
        "Usuario",
        backref="rol",
        lazy=True
    )