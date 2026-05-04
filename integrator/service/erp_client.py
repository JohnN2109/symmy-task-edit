import json
from pathlib import Path


def load_products():
    file_path = Path("data/products.json")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)