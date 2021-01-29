from django.shortcuts import render
from django.http import HttpResponse

from .utils import setPageActive
from .utils import setPageActiveuser
sidebar_pages = [
    {
        'name': 'Dashboard',
        'icon': 'home',
        'active': False,
        'link': 'rainhahome'
    },
    {
        'name': 'Saldo consumidores',
        'icon': 'users',
        'active': False,
        'link': 'RainhaSaldoCons'
    },   
    {
        'name': 'Estoque',
        'icon': 'house',
        'active': False,
        'link': 'estoque'
    },
    {
        'name': 'Inventário',
        'icon': 'house',
        'active': False,
        'link': 'inventario'
    }
]

sidebar_pages_user = [
    {
        'name': 'Dashboard',
        'icon': 'house',
        'active': False,
        'link': 'homeuser'
    },
    {
        'name': 'Carrinho',
        'icon': 'house',
        'active': False,
        'link': 'carrinho'
    },
    {
        'name': 'Pagamento',
        'icon': 'house',
        'active': False,
        'link': 'pagamento'
    }
]

global_context = {
    'sidebar_pages': sidebar_pages
}
context_user = {
    'sidebar_pages_user':sidebar_pages_user
}
# Create your views here.

def index(request):
    return render(request, 'lanchonete/index.html')

def dashboard(request):
    return HttpResponse('Dashboard')

def signin(request):
    return render(request, 'lanchonete/signin.html') 

def homeuser(request):
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'homeuser')
    return render(request, 'lanchonete/homeuser.html',context)

def pagamento(request):
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'pagamento')
    return render(request, 'lanchonete/pagamento.html',context)
    
def carrinho(request):
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'carrinho')
    return render(request, 'lanchonete/carrinho.html',context)

def estoque(request):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context = setPageActive(context,'estoque')
    return render(request, 'lanchonete/estoque.html',context)

def inventario(request):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context = setPageActive(context,'inventario')
    return render(request, 'lanchonete/inventario.html',context)

def historico(request):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context = setPageActive(context,'historico')
    return render(request, 'lanchonete/historico.html',context)

def rainhahome(request):
    context = {**global_context,  'nome_de_usuario': 'Thalles'}
    context = setPageActive(context, 'rainhahome')
    return render(request, 'lanchonete/rainhahome.html',context)

def rainhahomediscretiza(request):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context = setPageActive(context,'RainhaHomeDiscretiza')
    return render(request, 'lanchonete/RainhaHomeDiscretiza.html',context)

def RainhaSaldoCons(request):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context = setPageActive(context,'RainhaSaldoCons')
    return render(request, 'lanchonete/RainhaSaldoCons.html',context)

def RainhaSaldoConsDetalhe(request):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context = setPageActive(context,'RainhaSaldoConsDetalhe')
    return render(request, 'lanchonete/RainhaSaldoConsDetalhe.html',context)