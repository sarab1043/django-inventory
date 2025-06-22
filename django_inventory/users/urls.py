from django.urls import path
from users.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', UserProfileView.as_view(), name="user_profile"),
    path('update/', UserProfileView.as_view(), name="update_profile"),
    # user address
    path('get_address/', UserAddressView.as_view(), name="get_address"),
    path('add_address/', UserAddressView.as_view(), name="add_address"),
    path('update_address/<int:id>/', UserAddressView.as_view(), name="update_address"),
    # user orders
    path('orders/', UserOrdersView.as_view(), name="user_orders"),
    path('order/<int:id>/', GetUserOrderView.as_view(), name="order_by_id")
]


