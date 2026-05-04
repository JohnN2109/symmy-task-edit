import hashlib
import logging
import time

from integrator.models import ProductSync

logger = logging.getLogger(__name__)


def generate_hash(product):
    return hashlib.sha256(str(product).encode()).hexdigest()


def validate_product(product, seen_skus):
    sku = product.get("id")
    price = product.get("price_vat_excl")
    stocks = product.get("stocks", {})

    if sku in seen_skus:
        logger.warning(f"Duplicate SKU skipped: {sku}")
        return False

    seen_skus.add(sku)

    if price is None or price < 0:
        logger.warning(f"Invalid price skipped: {sku}")
        return False

    for stock in stocks.values():
        if not isinstance(stock, int):
            logger.warning(f"Invalid stock skipped: {sku}")
            return False

    return True


def transform_product(product):
    return {
        "sku": product["id"],
        "name": product["title"],
        "price": product["price_vat_excl"],
        "stock_total": sum(product.get("stocks", {}).values()),
        "attributes": product.get("attributes") or {},
    }


def mock_api_call(product):
    logger.warning(f"Mock API request simulated for: {product['sku']}")
    time.sleep(0.2)


def run_sync(products):
    seen_skus = set()

    for product in products:

        if not validate_product(product, seen_skus):
            continue

        transformed = transform_product(product)

        product_hash = generate_hash(transformed)

        obj, created = ProductSync.objects.get_or_create(
            sku=transformed["sku"],
            defaults={"payload_hash": product_hash},
        )

        if not created and obj.payload_hash == product_hash:
            logger.info(f"No changes detected: {transformed['sku']}")
            continue

        mock_api_call(transformed)

        obj.payload_hash = product_hash
        obj.save()

        logger.warning(f"Synced product: {transformed['sku']}")