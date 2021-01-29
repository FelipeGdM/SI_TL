from django.shortcuts import render
from django.http import HttpResponse

from .utils import setPageActive

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

global_context = {
    'sidebar_pages': sidebar_pages
}
# Create your views here.

def index(request):
    return render(request, 'lanchonete/index.html')

def dashboard(request):
    return HttpResponse('Dashboard')

def signin(request):
    return render(request, 'lanchonete/signin.html') 

def homeuser(request):
    return render(request, 'lanchonete/homeuser.html')

def pagamento(request):
    return render(request, 'lanchonete/pagamento.html')
    
def carrinho(request):
    return render(request, 'lanchonete/carrinho.html')

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