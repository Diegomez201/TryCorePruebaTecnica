from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nit = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100))
    estado = db.Column(db.String(20), default="PENDIENTE")  # PENDIENTE, PROCESADO, ERROR

    def __repr__(self):
        return f"<Empresa {self.nit}>"


        