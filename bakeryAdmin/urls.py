from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from bakeryAdmin import views

router = routers.DefaultRouter()
router.register(r'measure-unit', views.MeasureUnitView)
router.register(r'ingredient', views.IngredientView)
router.register(r'fixed-cost', views.FixedCostView)
router.register(r'recipe', views.RecipeView)
router.register(r'recipe-detail', views.RecipeDetailView)
router.register(r'recipe-detail-product', views.RecipeDetailProductView)
router.register(r'supplier', views.SupplierView)
router.register(r'make', views.MakeView)
router.register(r'supplier-invoice', views.SupplierInvoiceView)
router.register(r'supplier-invoice-detail', views.SupplierInvoiceDetailView)
router.register(r'production-order', views.ProductionOrderView)
router.register(r'production-order-detail', views.ProductionOrderDetailView)
router.register(r'product', views.ProductView)
router.register(r'product-stock', views.ProductStockView)


urlpatterns = [
    path("api/v1/", include(router.urls)),
    #path('docs/', include_docs_urls(title="BakeryAdmin API"))
]