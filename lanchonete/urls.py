from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard' ),
    path('signin', views.signin, name='signin' ),
    path('homeuser', views.homeuser, name='homeuser' ),
    path('pagamento', views.pagamento, name='pagamento' ),
    path('carrinho', views.carrinho, name='carrinho' ),
    path('rainhahome', views.rainhahome, name='rainhahome' ),
    path('rainhahomediscretiza', views.rainhahomediscretiza, name='rainhahomediscretiza' ),
    path('RainhaSaldoCons', views.RainhaSaldoCons, name='RainhaSaldoCons'),
    path('RainhaSaldoConsDetalhe', views.RainhaSaldoConsDetalhe, name='RainhaSaldoConsDetalhe'),
]