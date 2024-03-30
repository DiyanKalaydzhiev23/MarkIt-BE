from django.urls import path
from auth_app.views import UserCreateView, LoginUserView, LogoutUserView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
