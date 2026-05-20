from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cars/create/', views.car_create, name='car_create'),
    path('cars/<uuid:pk>/edit/', views.car_update, name='car_update'),
    path('cars/<uuid:pk>/delete/', views.car_delete, name='car_delete'),
]