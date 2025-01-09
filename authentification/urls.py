from django.urls import path 

from . import views

app_name = "authentification"

urlpatterns = [

    path('', views.HomeView.as_view(), name='login' ),
    path('signin', views.SigninView.as_view(), name='signin' ),
    path('logout', views.logout_view, name="logout"),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    # path('password-change/done/', TemplateView.as_view(template_name="authentification/password_change_done.html"), name='password_change_done'),

]