from dataclasses import dataclass
from typing import List
import datetime
from django.utils import timezone

from bakeryAdmin.domain.models.production.IngredientConsumeByRecipeDetail import IngredientConsumeByRecipeDetail

@dataclass
class IngredientConsumeByProductionOrderDetail:
    productionOrderDetail_id: int
    ingredientsConsumesByRecipeDetail: List[IngredientConsumeByRecipeDetail]
    expirationDate: datetime.datetime
    costPrice: float
    sellPrice: float
    batch: str

    @classmethod
    def of(self, productionOrderDetailId):
        return IngredientConsumeByProductionOrderDetail(
            productionOrderDetail_id = productionOrderDetailId,
            ingredientsConsumesByRecipeDetail = [],
            expirationDate=timezone.now(),
            costPrice=0,
            sellPrice=0,
            batch=""
        )