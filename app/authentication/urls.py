from django.urls import path

from . import views
from .views import signUpPage,loginPage

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('sign-up/', signUpPage.as_view(), name='signin'),
    path('login/',loginPage.as_view(),name = 'login'),
    path('logout/', views.logoutUser, name="logout"),
]