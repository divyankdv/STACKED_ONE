"""
============================================================

                STACKED QUANT AI V6

                    LOGGER

Central logging utility.

============================================================
"""

import logging
import os

LOG_FOLDER = "logs"

os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_FOLDER,
    "stacked_quant_ai.log",
)

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

    handlers=[

        logging.FileHandler(LOG_FILE),

        logging.StreamHandler(),

    ],

)

logger = logging.getLogger("STACKED")