from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop_product_search/', views.shop_product_search, name='shop_product_search'),
    path('product_search/', views.product_search, name="product_search"),
    path('category_search/<slug:slug>/', views.category_search, name="category_search"),
    path('product_detail/<slug:slug>/', views.product_detail, name="product_detail"),
    path('productItem_card/<slug:slug>/', views.productItem_card, name="productItem_card"),
    path('card/', views.card, name='card'),
    path('card_add/<slug:slug>/<int:quantity>/', views.card_add, name='card_add'),
    path('card_remove/<int:id>/', views.card_remove, name='card_remove'),
    path('card_update/<int:id>/', views.card_update, name='card_update'),
    path('card_clear/', views.card_clear, name='card_clear'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
]
