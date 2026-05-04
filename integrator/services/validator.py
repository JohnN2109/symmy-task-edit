def validate_product(product, processed_skus):
    sku = product.get("id")
    price = product.get("price_vat_excl")
    stocks = product.get("stocks", {})

    if not sku:
        return False, "Missing SKU"

    if sku in processed_skus:
        return False, "Duplicate SKU"

    if price is None or price < 0:
        return False, "Invalid price"

    for stock_value in stocks.values():
        if not isinstance(stock_value, int):
            return False, "Invalid stock"

    return True, None