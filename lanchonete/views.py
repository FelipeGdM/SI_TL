from django.shortcuts import render
from django.http import HttpResponse

from .utils import setPageActive
from .utils import setPageActiveuser
sidebar_pages = [
    {
        'name': 'Inventário',
        'icon': 'house',
        'active': False,
        'link': 'inventario'
    },
    {
        'name': 'Carrinho',
        'icon': 'house',
        'active': False,
        'link': 'carrinho'
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
    return render(request, 'lanchonete/homeuser.html',context_user)

def pagamento(request):
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'pagamento')
    return render(request, 'lanchonete/pagamento.html',context_user)
    
def carrinho(request):
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'carrinho')
    return render(request, 'lanchonete/carrinho.html',context_user)

def estoque(request):
    return render(request, 'lanchonete/estoque.html')

def inventario(request):
    return render(request, 'lanchonete/inventario.html')

def rainhahome(request):
    context = {**global_context,  'nome_de_usuario': 'Thalles'}
    context = setPageActive(context, 'Rainha Home')
    return render(request, 'lanchonete/rainhahome.html', global_context)

def rainhahomediscretiza(request):
    return render(request, 'lanchonete/RainhaHomeDiscretiza.html')

def RainhaSaldoCons(request):
    return render(request, 'lanchonete/RainhaSaldoCons.html')

def RainhaSaldoConsDetalhe(request):
    return render(request, 'lanchonete/RainhaSaldoConsDetalhe.html')