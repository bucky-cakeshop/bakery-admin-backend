

from dataclasses import dataclass

from bakeryAdmin.domain.models.production.AggregatedTotalProduct import AggregatedTotalProduct


@dataclass
class ProductionOrderMissingProductItem:
    aggregatedTotalProduct:AggregatedTotalProduct
    totalQuantityInStock:float
    totalToConsume:float
