import os

from dotenv import load_dotenv

from enums.currency import Currency
from enums.runtime_environment import RuntimeEnvironment
from external_ip import get_sslipio_external_url
from ngrok_executor import start_ngrok

load_dotenv(".env")
RUNTIME_ENVIRONMENT = RuntimeEnvironment(os.environ.get("RUNTIME_ENVIRONMENT"))
if RUNTIME_ENVIRONMENT == RuntimeEnvironment.DEV:
    WEBHOOK_HOST = start_ngrok()
else:
    WEBHOOK_HOST = get_sslipio_external_url()
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")
WEBAPP_HOST = os.environ.get("WEBAPP_HOST")
WEBAPP_PORT = int(os.environ.get("WEBAPP_PORT"))
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
TOKEN = os.environ.get("TOKEN")
ADMIN_ID_LIST = os.environ.get("ADMIN_ID_LIST").split(',')
ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID_LIST]
SUPPORT_LINK = os.environ.get("SUPPORT_LINK")
DB_ENCRYPTION = os.environ.get("DB_ENCRYPTION", False) == 'true'
DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")
PAGE_ENTRIES = int(os.environ.get("PAGE_ENTRIES"))
BOT_LANGUAGE = os.getenv("BOT_LANGUAGE", "tr")
MULTIBOT = os.environ.get("MULTIBOT", False) == 'true'
CURRENCY = Currency(os.environ.get("CURRENCY"))


# Binance Pay API ayarları
# BINANCE_PAY_API_KEY = os.getenv("BINANCE_PAY_API_KEY", "")
# BINANCE_PAY_API_SECRET = os.getenv("BINANCE_PAY_API_SECRET", "")
# BINANCE_PAY_WEBHOOK_URL = os.getenv("BINANCE_PAY_WEBHOOK_URL", f"{WEBHOOK_URL}processing/binance-pay/webhook")

# KRYPTO_EXPRESS_API_KEY = os.getenv("KRYPTO_EXPRESS_API_KEY", "")
# KRYPTO_EXPRESS_API_SECRET = os.getenv("KRYPTO_EXPRESS_API_SECRET", "")
# KRYPTO_EXPRESS_API_URL = os.getenv("KRYPTO_EXPRESS_API_URL", "")

# NOWPayments Configuration
NOWPAYMENTS_API_KEY = "PG74S32-81EMFW9-JZXGXQR-5B8ZABM"
NOWPAYMENTS_IPN_SECRET = "82134ea6-522d-4dbe-8aac-15bda5e5db8d"
NOWPAYMENTS_WEBHOOK_URL = f"{WEBHOOK_URL}processing/nowpayments/webhook"

WEBHOOK_SECRET_TOKEN = os.environ.get("WEBHOOK_SECRET_TOKEN")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")