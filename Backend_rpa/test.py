import json
from app import app

def test_home():
    tester = app.test_client()
    response = tester.get("/")
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "API RPA funcionando"

def test_process_data():
    tester = app.test_client()
    payload = {"nit": "123456789", "nombre": "Empresa Prueba"}
    response = tester.post("/process-data", 
                           data=json.dumps(payload), 
                           content_type="application/json")
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Datos procesados y almacenados correctamente"
