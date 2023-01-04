from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('product', views.product, name='product'),
    path('productCreate', views.productCreate, name='productCreate'),
    path('productUpdate/<slug:slug>/', views.productUpdate, name='productUpdate'),
    path('productDelete/<slug:slug>/', views.productDelete, name='productDelete'),
    
    path('productItem', views.productItem, name='productItem'),
    path('productItemCreate', views.productItemCreate, name='productItemCreate'),
    path('productItemUpdate/<slug:slug>/', views.productItemUpdate, name='productItemUpdate'),
    path('productItemDelete/<slug:slug>/', views.productItemDelete, name='productItemDelete'),

    path('productColor', views.productColor, name='productColor'),
    path('productColorCreate', views.productColorCreate, name='productColorCreate'),
    path('productColorUpdate/<int:id>/', views.productColorUpdate, name='productColorUpdate'),
    path('productColorDelete/<int:id>/', views.productColorDelete, name='productColorDelete'),

    path('productSize', views.productSize, name='productSize'),
    path('productSizeCreate', views.productSizeCreate, name='productSizeCreate'),
    path('productSizeUpdate/<int:id>/', views.productSizeUpdate, name='productSizeUpdate'),
    path('productSizeDelete/<int:id>/', views.productSizeDelete, name='productSizeDelete'),

    path('brand', views.brand, name='brand'),
    path('brandCreate', views.brandCreate, name='brandCreate'),
    path('brandUpdate/<slug:slug>/', views.brandUpdate, name='brandUpdate'),
    path('brandDelete/<slug:slug>/', views.brandDelete, name='brandDelete'),

    path('category', views.category, name='category'),
    path('categoryCreate', views.categoryCreate, name='categoryCreate'),
    path('categoryUpdate/<slug:slug>/', views.categoryUpdate, name='categoryUpdate'),
    path('categoryDelete/<slug:slug>/', views.categoryDelete, name='categoryDelete'),

    path('productCommet/<slug:slug>/', views.productCommet, name='productCommet')
]
