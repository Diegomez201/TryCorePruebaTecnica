import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from utils import log_info

def enviar_reporte_email(to_email, subject, body, attachment_path=None):
    
    log_info("Correo enviado.")
