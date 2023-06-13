from dataclasses import dataclass

@dataclass
class AggregatedProduct:
    productId: int
    productName: str
    measureUnitId: int
    measureUnitSymbol: str
    quantity: float
    recipeQuantity: float
    
    @property
    def total(self):
        return self.quantity*self.recipeQuantity
