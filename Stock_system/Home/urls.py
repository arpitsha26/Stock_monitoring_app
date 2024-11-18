from django.urls import path
from .views import stocklist, subscribestock

urlpatterns = [
    path("stocks/", stocklist.as_view(), name="stock-list"),
    path("stocks/subscribe/", subscribestock.as_view(), name="subscribe-stock"),
]
