from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_clients/', views.dashboard_clients, name='dashboard_clients'),
    path('user_role/<int:pk>/', views.user_role, name='user_role'),
    path('profile_home/', views.profile_home, name='profile_home'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/<int:pk>/', views.profile_update, name='profile_update'),
    path('cardChange/<int:pk>', views.user_change_card, name='cardChange'),
    path('passChange/<int:pk>/', views.user_change_password, name='passChange'),
    path('addressChange/<int:pk>', views.user_change_address, name='addressChange'),
    path('user_delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('', views.user_login, name='user_login'),
]