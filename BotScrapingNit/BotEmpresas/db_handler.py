import json
from modelo import SessionLocal, Empresa, ConsultaResult, init_db

# Inicializar Base , Crea tablas asi no existan
def setup_database():
    init_db()

def get_empresa(nit):
    session = SessionLocal()
    e = session.query(Empresa).filter_by(nit=nit).first()
    session.close()
    return e

def create_or_get_empresa(nit, nombre=None):
    session = SessionLocal()
    e = session.query(Empresa).filter_by(nit=nit).first()
    if not e:
        e = Empresa(nit=nit, nombre=nombre, estado="PENDIENTE")
        session.add(e)
        session.commit()
        session.refresh(e)
    session.close()
    return e

def update_estado(nit, estado):
    session = SessionLocal()
    e = session.query(Empresa).filter_by(nit=nit).first()
    if e:
        e.estado = estado
        session.commit()
    session.close()

def save_result(nit, result_dict):
    session = SessionLocal()
    cr = ConsultaResult(nit=nit, data=json.dumps(result_dict))
    session.add(cr)
    session.commit()
    session.close()
