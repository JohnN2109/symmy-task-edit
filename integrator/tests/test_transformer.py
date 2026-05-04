from integrator.services.transformer import transform_product


def test_stock_sum():
    product = {
        "id": "SKU-001",
        "title": "Coffee",
        "price_vat_excl": 100,
        "stocks": {
            "praha": 5,
            "brno": 3,
        },
    }

    transformed = transform_product(product)

    assert transformed["stock"] == 8