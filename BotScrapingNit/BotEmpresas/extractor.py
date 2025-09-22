from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils import save_screenshot, log_info, log_error, retry
from selenium.webdriver.common.alert import Alert

#Ruta de chromedriver
CHROMEDRIVER_PATH = r"C:\Users\GMZ_DELL\Desktop\Try\BotEmpresas\Drivers\chromedriver-win64\chromedriver.exe"

#configuradciones del navegador
def build_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1200, 900)
    return driver


@retry(max_attempts=3, delay=2)
def consultar_rues(nit, headless=False, timeout=15):

    driver = build_driver(headless=headless)
    try:
        driver.get("https://www.rues.org.co/?old=true")
        wait = WebDriverWait(driver, timeout)

        #Cerrar mensaje si aparece 
        try:
            close_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='swal2-close']"))
            )
            close_button.click()
        except TimeoutException:
            pass  # si no aparece se continua

        # Txt de búsqueda 
        input_box = wait.until(EC.presence_of_element_located((By.ID, "search")))
        input_box.clear()
        input_box.send_keys(nit)

        # Botón buscar
        boton_buscar = driver.find_element(By.XPATH, "//button[contains(text(),'Buscar')]")
        boton_buscar.click()

        # Esperar resultados con un wait
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "p.font-rues--large.filtro__titulo")
            )
        )

        # Capturar datos arrojados del NIT consultado
        data = {}
        try:
            data["nombre"] = driver.find_element(
                By.CSS_SELECTOR, "p.font-rues--large.filtro__titulo"
            ).text
        except NoSuchElementException:
            data["nombre"] = ""

        campos_xpath = {
            "identificacion": "//div[@class='registroapi'][p[text()='Identificación']]/span",
            "numero_inscripcion": "//div[@class='registroapi'][p[text()='Numero de Inscripción']]/span",
            "categoria": "//div[@class='registroapi'][p[text()='Categoria']]/span",
            "camara_comercio": "//div[@class='registroapi'][p[text()='Cámara de Comercio']]/span",
            "numero_matricula": "//div[@class='registroapi'][p[text()='Número de Matrícula']]/span",
            "estado": "//div[@class='registroapi'][p[text()='Estado']]/span",
        }

        for campo, xpath in campos_xpath.items():
            try:
                data[campo] = driver.find_element(By.XPATH, xpath).text
            except NoSuchElementException:
                data[campo] = ""

        data["_fetched_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        #print("Datos extraídos:", data)
        return data

    except Exception as e:
        save_screenshot(driver, name_prefix=f"error_{nit}")
        log_error(f"Error consultando RUES para {nit}: {e}")
        raise
    finally:
        driver.quit()
