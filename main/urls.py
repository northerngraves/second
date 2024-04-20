from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('complete/', views.complete, name='complete'),

    path('update_item/', views.updateItem, name='update_item'),
    path('update_checkout/', views.updateCheckout, name='update_checkout'),
]