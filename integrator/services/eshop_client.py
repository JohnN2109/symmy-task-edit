import logging
import time

logger = logging.getLogger(__name__)


def send_product(product):
    time.sleep(0.2)

    logger.warning(
        "Mock API request simulated",
        extra={
            "sku": product["sku"],
        }
    )

    return True