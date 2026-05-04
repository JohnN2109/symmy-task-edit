from dataclasses import dataclass


@dataclass
class ProductDTO:
    sku: str
    title: str
    price: float
    stock: int