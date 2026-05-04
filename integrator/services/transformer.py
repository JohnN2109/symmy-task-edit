def transform_product(product):
    total_stock = sum(product.get("stocks", {}).values())

    return {
        "sku": product["id"],
        "name": product["title"],
        "price": product["price_vat_excl"],
        "stock": total_stock,
        "attributes": product.get("attributes") or {},
    }