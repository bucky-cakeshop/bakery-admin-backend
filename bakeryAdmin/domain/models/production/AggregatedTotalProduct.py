from dataclasses import dataclass

@dataclass
class AggregatedTotalProduct:
    productId: int
    productName: str
    measureUnitId: int
    measureUnitSymbol: str
    total: float

