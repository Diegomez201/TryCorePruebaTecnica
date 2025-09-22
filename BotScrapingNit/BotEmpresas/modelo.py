import os
import pathlib
import datetime
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = pathlib.Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nit = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=True)
    estado = Column(String, default="PENDIENTE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ConsultaResult(Base):
    __tablename__ = "consulta_results"
    id = Column(Integer, primary_key=True)
    nit = Column(String, ForeignKey("empresas.nit"))
    data = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
