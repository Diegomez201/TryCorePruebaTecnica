from pathlib import Path
import pandas as pd

# Ruta base desde la Raiz tanto de en ENtrada como en Output
BASE_DIR = Path(__file__).parent  

INPUT_DIR = BASE_DIR / "Entrada"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def read_empresas_xlsx(filename="Empresas_Nit.xlsx"):
    path = INPUT_DIR / filename
    df = pd.read_excel(path, dtype=str) 
    df = df.fillna("") 
    if "NIT" not in df.columns:
        raise ValueError("El archivo de entrada debe contener la columna 'NIT'.")
    return df

def save_reporte(df, filename="reporte_final.xlsx"):
    path = OUTPUT_DIR / filename
    df.to_excel(path, index=False)
    return path
