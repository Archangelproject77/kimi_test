from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.home,name='home'),
    path('shop/', views.product_list, name='product_list'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    #cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    #order
    path('create/', views.order_create, name='order_create'),
    #coupon
    path('apply/', views.coupon_apply, name='apply'),
    
    #-------------------------------------
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
]