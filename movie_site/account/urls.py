from django.urls import path
from .views import registration_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView ,TokenBlacklistView

urlpatterns = [
 
    path('register/',registration_view,name='register'),
    path('logout/',TokenBlacklistView.as_view(), name='token_blacklist'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
