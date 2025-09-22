import pandas as pd
from file_handler import read_empresas_xlsx, save_reporte
from db_handler import setup_database, create_or_get_empresa, update_estado, save_result
from extractor import consultar_rues
from utils import log_info, log_error
from notifier import enviar_reporte_email
import os

def run_bot(headless=False, email_report_to=None):
    log_info("Iniciando bot")
    setup_database()

    df = read_empresas_xlsx()
    results = []

    for idx, row in df.iterrows():
        nit = str(row.get("NIT")).strip()
        nombre = row.get("NombreEmpresa", "")
        if not nit:
            log_error(f"Fila {idx+2}: NIT vacío. Se marca ERROR.")
            update_estado("", "ERROR")
            continue

        # Crear registro Asi no exista
        create_or_get_empresa(nit, nombre)
        update_estado(nit, "PENDIENTE")

        try:
            # Ejecutar consulta 
            data = consultar_rues(nit, headless=headless)
            # Guardar resultados en Base 
            save_result(nit, data)
            update_estado(nit, "PROCESADO")
            results.append({"NIT": nit, "NombreEmpresa": nombre, "Estado": "PROCESADO", **data})
        except Exception as e:
            log_error(f"Error en procesamiento de {nit}: {e}")
            update_estado(nit, "ERROR")
            results.append({"NIT": nit, "NombreEmpresa": nombre, "Estado": "ERROR", "error": str(e)})

    # Generar DataFrame y guardar reporte en outputs
    df_out = pd.DataFrame(results)
    out_path = save_reporte(df_out, filename="reporte_final.xlsx")
    log_info(f"Reporte guardado en {out_path}")

    # Notificar por correo No lo termine de configurar por que me pide doble auteticacion, Metodo vacio
    if email_report_to:
        body = f"Reporte de ejecución. Filas procesadas: {len(results)}"
        try:
            enviar_reporte_email(email_report_to, "Reporte Bot RUES", body, attachment_path=out_path)
        except Exception as e:
            log_error(f"No se pudo enviar correo: {e}")

    log_info("Ejecución finalizada.")


if __name__ == "__main__":
    # Ejecución local: puedes pasar headless True/False y correo por env o cambiar aquí.
    EMAIL = os.getenv("REPORT_TO")  # ejemplo: set REPORT_TO=mi@mail.com
    run_bot(headless=False, email_report_to=EMAIL)
