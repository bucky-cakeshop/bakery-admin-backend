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
urlpatterns = [
    path("api/v1/", include(router.urls)),
    #path('docs/', include_docs_urls(title="BakeryAdmin API"))
]