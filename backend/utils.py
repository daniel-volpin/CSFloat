import logging
import os
from dotenv import load_dotenv

# Load .env from backend directory if present, falling back to CWD search
_here = os.path.dirname(__file__)
backend_env = os.path.join(_here, ".env")
if os.path.exists(backend_env):
    load_dotenv(dotenv_path=backend_env)
else:
    load_dotenv()

API_KEY = os.getenv("CSFLOAT_API_KEY")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def get_api_key():
    if not API_KEY:
        logger.error("CSFLOAT_API_KEY not set in environment.")
        raise ValueError("API key not configured.")
    return API_KEY
