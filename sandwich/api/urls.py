from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import *

router = DefaultRouter()
router.register('bread', BreadViewSet, basename="bread")
router.register('topping', ToppingViewSet, basename="topping")
router.register('cheese', CheeseViewSet, basename="cheese")
router.register('sauce', SauceViewSet, basename="sauce")
router.register('sandwich', SandwichViewSet, basename="sandwich")

app_name = "api"
urlpatterns = [
    # api
    path("", include(router.urls)),
]
