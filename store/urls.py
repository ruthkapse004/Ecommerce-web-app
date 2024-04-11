from django.urls import path
from . import views


urlpatterns = [
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('place_order/', views.place_order, name='place_order'),
]
