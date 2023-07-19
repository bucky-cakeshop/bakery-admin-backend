from dataclasses import dataclass
from typing import List
import datetime
from django.utils import timezone

from bakeryAdmin.domain.models.production.ConsumeByRecipeDetail import ConsumeByRecipeDetail

@dataclass
class ConsumeByProductionOrderDetail:
    productionOrderDetail_id: int
    consumesByRecipeDetail: List[ConsumeByRecipeDetail]
    expirationDate: datetime.datetime
    costPrice: float
    sellPrice: float
    batch: str

    @classmethod
    def of(self, productionOrderDetailId):
        return ConsumeByProductionOrderDetail(
            productionOrderDetail_id = productionOrderDetailId,
            consumesByRecipeDetail = [],
            expirationDate=timezone.now(),
            costPrice=0,
            sellPrice=0,
            batch=""
        )