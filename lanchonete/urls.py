from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('estoque', views.estoque, name='estoque'),
    path('inventario', views.inventario, name='inventario'),
    path('historico/<int:id>', views.historico, name='historico'),
    path('signin', views.signin, name='signin'),
    path('homeuser',views.homeuser, name='homeuser'),
    path('pagamento',views.pagamento, name='pagamento'),
    path('carrinho',views.carrinho, name='carrinho'),
    path('RainhaSaldoConsDetalhe', views.RainhaSaldoConsDetalhe, name='RainhaSaldoConsDetalhe'),
    path('RainhaSaldoCons', views.RainhaSaldoCons, name='RainhaSaldoCons'),
    path('rainhahomediscretiza', views.rainhahomediscretiza, name='rainhahomediscretiza' ),
    path('rainhahome', views.rainhahome, name='rainhahome'),
    path('produto/delete/<int:id>', views.produtoDelete, name='produtoDelete'),
    path('produto/edit/<int:id>/<str:disponibilidade>/<str:nome_editar>/<int:preco_editar>/<int:estoque_editar>',views.produtoEdit, name='produtoEdit')
]