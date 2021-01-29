from django.shortcuts import render
from django.http import HttpResponse

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

def RainhaSaldoConsDetalhe(request):
def RainhaSaldoCons(request):
def rainhahomediscretiza(request):
def rainhahome(request):