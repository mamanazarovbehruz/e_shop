from django.urls import path
from . import views

app_name = 'deliveries'

urlpatterns = [
    path('deli',views.deli, name='deli')
]
