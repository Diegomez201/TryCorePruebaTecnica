from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from modelo import db, Empresa


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Crear la base de datos
with app.app_context():
    db.create_all()

# --- Endpoint raíz de bienvenida para validar desde navegador---
@app.route("/", methods=["GET"])
def home():
    return {"message": "API RPA funcionando"}

# --- Endpoint 1: Procesar datos(Insrtar infomacion) ---
@app.route("/process-data", methods=["POST"])
def process_data():
    try:
        data = request.get_json()
        if not data or "nit" not in data or "nombre" not in data:
            return jsonify({"error": "Datos inválidos"}), 400

        empresa = Empresa.query.filter_by(nit=data["nit"]).first()
        if empresa:
            return jsonify({"error": "La empresa ya existe"}), 400

        nueva_empresa = Empresa(nit=data["nit"], nombre=data["nombre"])
        db.session.add(nueva_empresa)
        db.session.commit()

        return jsonify({"message": "Empresa registrada correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Endpoint 2: Actualizar estado(Se envia el nit y el estado) ---
@app.route("/update-status", methods=["POST"])
def update_status():
    try:
        data = request.get_json()
        if not data or "nit" not in data or "estado" not in data:
            return jsonify({"error": "Datos inválidos"}), 400

        empresa = Empresa.query.filter_by(nit=data["nit"]).first()
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404

        empresa.estado = data["estado"]
        db.session.commit()

        return jsonify({"message": "Estado actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)