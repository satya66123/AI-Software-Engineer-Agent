import logging
import os

LOG_DIR = "src/logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create logs folder if absent
os.makedirs(LOG_DIR, exist_ok=True)

# Create app.log only if absent
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        pass

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    force=True
)

logger = logging.getLogger(__name__)

logger.info("Logger initialized")