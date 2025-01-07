from django.urls import path 

from . import views

app_name = "authentification"

urlpatterns = [

    path('', views.HomeView.as_view(), name='login' ),
    path('signin', views.SigninView.as_view(), name='signin' ),
    path('logout', views.logout_view, name="logout"),
]