from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist_add/<slug:slug>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_delete/<int:id>/', views.wishlist_delete, name='wishlist_delete'),
]
