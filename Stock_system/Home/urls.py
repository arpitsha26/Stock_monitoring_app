from django.urls import path
from .views import stocklist, subscribestock, SignUpView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("stocks/", stocklist.as_view(), name="stock-list"),
    path("stocks/subscribe/", subscribestock.as_view(), name="subscribe-stock"),
    path('signup/',SignUpView.as_view(), name="signup" )
]
