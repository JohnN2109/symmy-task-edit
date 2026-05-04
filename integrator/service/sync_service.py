import hashlib
import json
import logging

from integrator.models import ProductSync
from integrator.services.erp_client import load_products
from integrator.services.validator import validate_product
from integrator.services.transformer import transform_product
from integrator.services.eshop_client import send_product

logger = logging.getLogger(__name__)


def generate_hash(data):
    payload = json.dumps(data, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def run_sync():
    products = load_products()

    processed_skus = set()

    synced = 0
    skipped = 0
    invalid = 0

    for product in products:
        sku = product.get("id")

        is_valid, error = validate_product(product, processed_skus)

        if not is_valid:
            logger.warning(f"{error} skipped: {sku}")
            invalid += 1
            continue

        processed_skus.add(sku)

        transformed = transform_product(product)

        product_hash = generate_hash(transformed)

        obj, created = ProductSync.objects.get_or_create(
            sku=transformed["sku"],
            defaults={"last_hash": product_hash},
        )

        if not created and obj.last_hash == product_hash:
            logger.info(f"No changes detected: {sku}")
            skipped += 1
            continue

        send_product(transformed)

        obj.last_hash = product_hash
        obj.save()

        logger.warning(f"Synced product: {sku}")

        synced += 1

    logger.info(
        f"Sync completed | synced={synced} skipped={skipped} invalid={invalid}"
    )