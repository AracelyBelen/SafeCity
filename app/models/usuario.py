from app.extensions import db
from flask_login import UserMixin

class Usuario(
    UserMixin,
    db.Model
):

    __tablename__ = "usuarios"

    id_usuario = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    apellido = db.Column(
        db.String(100),
        nullable=False
    )

    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    fecha_registro = db.Column(
        db.DateTime
    )

    id_rol = db.Column(
        db.Integer,
        db.ForeignKey(
            "roles.id_rol"
        ),
        nullable=False
    )

    def get_id(self):
        return str(
            self.id_usuario
        )