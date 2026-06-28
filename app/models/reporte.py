from app.extensions import db

class Reporte(db.Model):

    __tablename__ = "reportes"

    id_reporte = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(200),
        nullable=False
    )

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    fecha_reporte = db.Column(
        db.DateTime
    )

    fecha_actualizacion = db.Column(
        db.DateTime
    )

    latitud = db.Column(
        db.Float
    )

    longitud = db.Column(
        db.Float
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuarios.id_usuario"
        )
    )

    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey(
            "categorias.id_categoria"
        )
    )
    
    evidencias = db.relationship(
        "Evidencia",
        backref="reporte",
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    categoria = db.relationship(
        "Categoria",
        backref="reportes"
        
    )
    
    zonas = db.relationship(
        "ReporteZona",
        backref="reporte",
        lazy=True
    )