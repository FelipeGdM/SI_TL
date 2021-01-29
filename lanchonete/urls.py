from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('estoque', views.estoque, name='estoque'),
    path('inventario', views.inventario, name='inventario')
    path('signin', views.signin, name='signin'),
    path('homeuser',views.homeuser, name='homeuser'),
    path('pagamento',views.pagamento, name='pagamento'),
    path('carrinho',views.carrinho, name='carrinho')
]