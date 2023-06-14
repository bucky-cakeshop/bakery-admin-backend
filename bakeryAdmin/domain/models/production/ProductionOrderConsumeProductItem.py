from dataclasses import dataclass

@dataclass
class ProductionOrderConsumeProductItem:
    productionOrder_id: int
    productStock_id: int
    quantity: float

