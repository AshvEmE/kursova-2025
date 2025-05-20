from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('email-confirmation/', views.econfirm , name='econfirm'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
