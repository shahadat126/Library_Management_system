from django.urls import path
from .views import Login,Logout,Register_view
app_name = 'user'
urlpatterns = [
    path("login/",Login,name='user_login' ),
    path("logout/",Logout,name='user_logout' ),
    path("register_view/",Register_view,name= 'register'),
]