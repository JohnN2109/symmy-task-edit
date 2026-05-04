from integrator.services.validator import validate_product


def test_negative_price_invalid():
    product = {
        "id": "SKU-001",
        "price_vat_excl": -100,
        "stocks": {"praha": 5},
    }

    valid, error = validate_product(product, set())

    assert valid is False
    assert error == "Invalid price"


def test_duplicate_sku_invalid():
    product = {
        "id": "SKU-001",
        "price_vat_excl": 100,
        "stocks": {"praha": 5},
    }

    valid, error = validate_product(product, {"SKU-001"})

    assert valid is False
    assert error == "Duplicate SKU"