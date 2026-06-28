from app.extensions import db

class ReporteZona(db.Model):

    __tablename__ = "reporte_zona"

    id_reporte_zona = db.Column(
        db.Integer,
        primary_key=True
    )

    id_reporte = db.Column(
        db.Integer,
        db.ForeignKey(
            "reportes.id_reporte"
        )
    )

    id_zona = db.Column(
        db.Integer,
        db.ForeignKey(
            "zonas.id_zona"
        )
    )
    
    zona = db.relationship(
        "Zona",
        backref="reportes_zona"
    )