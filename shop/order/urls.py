from django.urls import path
from shop import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
]