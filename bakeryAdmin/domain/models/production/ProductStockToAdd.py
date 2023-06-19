import datetime
from dataclasses import dataclass

@dataclass
class ProductStockToAdd:
    productId: int
    measureUnitId: int
    quantity: float
    quantityConsumed: float
    isForSell: bool
    batch: str
    expirationDate: datetime.datetime
    unitCostPrice: float
    unitSellPrice: float


