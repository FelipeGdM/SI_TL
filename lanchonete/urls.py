from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('estoque', views.estoque, name='estoque'),
    path('inventario', views.inventario, name='inventario'),
    path('historico/<int:id>', views.historico, name='historico'),
    path('signin', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('homeuser',views.homeuser, name='homeuser'),
    path('pagamento',views.pagamento, name='pagamento'),
    path('carrinho',views.carrinho, name='carrinho'),
    path('RainhaSaldoConsDetalhe', views.RainhaSaldoConsDetalhe, name='RainhaSaldoConsDetalhe'),
    path('RainhaSaldoCons', views.RainhaSaldoCons, name='RainhaSaldoCons'),
    path('RainhaHomeDetalhe', views.RainhaHomeDetalhe, name='RainhaHomeDetalhe' ),
    path('RainhaHome', views.RainhaHome, name='RainhaHome'),
    path('produto/delete/<int:id>', views.produtoDelete, name='produto')
]