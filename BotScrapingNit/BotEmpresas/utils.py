import logging
from pathlib import Path
from functools import wraps
import time
from datetime import datetime

LOG_DIR = Path(__file__).parent.parent / "logs"
SCREEN_DIR = Path(__file__).parent.parent / "screenshots"
LOG_DIR.mkdir(parents=True, exist_ok=True)
SCREEN_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "bot_rpa.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def log_info(msg):
    logging.info(msg)
    print(msg)

def log_error(msg):
    logging.error(msg)
    print("ERROR:", msg)

def save_screenshot(driver, name_prefix="error"):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = SCREEN_DIR / f"{name_prefix}_{timestamp}.png"
    try:
        driver.save_screenshot(str(filename))
        log_info(f"Screenshot saved to {filename}")
    except Exception as e:
        log_error(f"No se pudo tomar screenshot: {e}")

def retry(max_attempts=3, delay=2, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            _delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    log_error(f"Intento {attempts}/{max_attempts} falló: {e}")
                    if attempts >= max_attempts:
                        raise
                    time.sleep(_delay)
                    _delay *= backoff
        return wrapper
    return decorator
