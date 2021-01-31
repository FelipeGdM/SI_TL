from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from .utils import setPageActive
from .utils import setPageActiveuser
from .models import Produto, Compra, UserTL,Pagamento, Evento, TipoEvento

sidebar_pages = [
    {
        'name': 'Dashboard',
        'icon': 'home',
        'active': False,
        'link': '/rainhahome'
    },
    {
        'name': 'Saldo consumidores',
        'icon': 'users',
        'active': False,
        'link': '/RainhaSaldoCons'
    },   
    {
        'name': 'Estoque',
        'icon': 'house',
        'active': False,
        'link': '/estoque'
    },
    {
        'name': 'Inventário',
        'icon': 'house',
        'active': False,
        'link': '/inventario'
    }
]

sidebar_pages_user = [
    {
        'name': 'Dashboard',
        'icon': 'house',
        'active': False,
        'link': '/homeuser'
    },
    {
        'name': 'Carrinho',
        'icon': 'house',
        'active': False,
        'link': '/carrinho'
    },
    {
        'name': 'Pagamento',
        'icon': 'house',
        'active': False,
        'link': '/pagamento'
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
    
    transacoes = [*list(Compra.objects.filter(user=UserTL(id=1))),*list(Pagamento.objects.filter(user=UserTL(id=1)))]
    #transacoes = transacoes.sort(key = lambda x:x['data'], reverse=True)
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'homeuser')
    context['transacoes'] = transacoes

    if request.method=='GET':
        return render(request, 'lanchonete/homeuser.html',context)

    elif request.method=='POST':
        form_data = request.POST.dict()
        if form_data.get('tipo_de_transacao') == 'tudo':
            transacoes = [*list(Compra.objects.filter(user=UserTL(id=1))),*list(Pagamento.objects.filter(user=UserTL(id=1)))]
            context['transacoes'] = transacoes

        if form_data.get('tipo_de_transacao') == 'compras':
            transacoes = Compra.objects.filter(user=UserTL(id=1))
            context['transacoes'] = transacoes

        if form_data.get('tipo_de_transacao') == 'pagamentos':
            transacoes = Pagamento.objects.filter(user=UserTL(id=1))
            context['transacoes'] = transacoes
        
        context['form_data'] = form_data
        return render(request, 'lanchonete/homeuser.html',context)

        #maracutaias legais

def pagamento(request):
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'pagamento')
    if request.method=='GET':
        return render(request, 'lanchonete/pagamento.html',context)

    elif request.method=='POST':
        form_data = request.POST.dict()
        context['pagamento_feito'] = False
        if form_data['forma_de_pagamento'] != '' and form_data['quantia_paga']!= '0':
            context['pagamento_feito'] = True
            Pagamento.objects.create(user=UserTL(id=1),especie=form_data['forma_de_pagamento'] , valor=form_data['quantia_paga'])     
            Evento.objects.create(info=f'Pagou {form_data["quantia_paga"]}TBs', tipo='Pagamento')

        return render(request, 'lanchonete/pagamento.html',context)

    
def carrinho(request):
    produto = {
        'salgado': Produto.objects.filter(tipo='salgado'),
        'doce': Produto.objects.filter(tipo='doce'),
        'bebida': Produto.objects.filter(tipo='bebida'),
    }
    context = {**context_user, 'nome_do_usuario':'Thalles', 'produtos': produto}
    context = setPageActiveuser(context,'carrinho')
    context['compra_finalizada'] = False
    context['compra_erro'] = False
    if request.method=='GET':
        return render(request, 'lanchonete/carrinho.html',context)

    elif request.method=='POST':
        form_data = request.POST.dict()

        produtos = []
        if form_data['salgado_tipo'] != '' and form_data['salgado_qtde'] != '0':
            produtos.append({
                'nome': form_data['salgado_tipo'],
                'quantidade': form_data['salgado_qtde'],
            })
        if form_data['doce_tipo'] != '' and form_data['doce_qtde'] != '0':
            produtos.append({
                'nome': form_data['doce_tipo'],
                'quantidade': form_data['doce_qtde'],
            })
        if form_data['bebida_tipo'] != '' and form_data['bebida_qtde'] != '0':
            produtos.append({
                'nome': form_data['bebida_tipo'],
                'quantidade': form_data['bebida_qtde'],
            })
        
        if len(produtos) > 0:
            valor_compra = 0
            for prod in produtos:
                Produto.objects.filter(nome=prod['nome']).update(estoque=F('estoque')-prod['quantidade'])
                Evento.objects.create(info=f'Comprou {prod["quantidade"]} de {prod["nome"]}', tipo="Compra")
                valor_compra += int(prod['quantidade'])*Produto.objects.filter(nome=prod['nome']).get().valor

            Compra.objects.create(user=UserTL(id=1), produtos=produtos, valor=valor_compra)
            context['compra_finalizada'] = True
            return render(request, 'lanchonete/carrinho.html', context)
        else:

            context['compra_finalizada'] = False
            context['compra_erro'] = True
            return render(request, 'lanchonete/carrinho.html', context)

    else:
        return HttpResponse('Requisição inválida!')

def estoque(request):
    produto = {
        'salgado': Produto.objects.filter(tipo='salgado', disponivel=True),
        'doce': Produto.objects.filter(tipo='doce', disponivel=True),
        'bebida': Produto.objects.filter(tipo='bebida', disponivel=True),
    }
    context = {**global_context, 'nome_do_usuario':'Thalles', 'produtos': produto}
    context = setPageActive(context,'estoque')
    if request.method=='GET':
        return render(request, 'lanchonete/estoque.html',context)
    
    elif request.method=='POST':
        form_data = request.POST.dict()

        if form_data['pesquisa'] == "todos":
            context['listagem_produtos'] = [*list(produto["salgado"]), *list(produto["doce"]), *list(produto["bebida"])]
        elif form_data['pesquisa'] == "salgado":
            context['listagem_produtos'] = [*list(produto["salgado"])]
        elif form_data['pesquisa'] == "doce":
            context['listagem_produtos'] = [*list(produto["doce"])]
        elif form_data['pesquisa'] == "bebida":
            context['listagem_produtos'] = [*list(produto["bebida"])]
        
        return render(request, 'lanchonete/estoque.html',context)

def inventario(request):
    produto = {
        'salgado': Produto.objects.filter(tipo='salgado'),
        'doce': Produto.objects.filter(tipo='doce'),
        'bebida': Produto.objects.filter(tipo='bebida'),
    }
    context = {**global_context, 'nome_do_usuario':'Thalles', 'produtos': produto}
    context = setPageActive(context,'inventario')
    context['item_adicionado'] = False

    if request.method=='GET':
        return render(request, 'lanchonete/inventario.html',context)
    
    elif request.method=='POST':
        form_data = request.POST.dict()

        if form_data['nome_do_formulario'] == "formulario_adicionar_item" and form_data['nome_do_item'] != '':
            Produto.objects.create(valor= form_data['preco'], estoque=  0, nome= form_data['nome_do_item'], tipo= form_data['categoria'])
            context['item_adicionado'] = True
        
        elif form_data['nome_do_formulario'] == "formulario_filtrar":
            if form_data['pesquisa'] == "todos":
                context['listagem_produtos'] = [*list(produto["salgado"]), *list(produto["doce"]), *list(produto["bebida"])]
            elif form_data['pesquisa'] == "salgado":
                context['listagem_produtos'] = [*list(produto["salgado"])]
            elif form_data['pesquisa'] == "doce":
                context['listagem_produtos'] = [*list(produto["doce"])]
            elif form_data['pesquisa'] == "bebida":
                context['listagem_produtos'] = [*list(produto["bebida"])]
        
        #elif form_data['nome_do_formulario'] == "formulario_alterar_inventario":
            

        return render(request, 'lanchonete/inventario.html',context)
    
    else:
        return HttpResponse('Requisição inválida!')
        
def produtoDelete(request, id=None):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context['id'] = id
    Produto.objects.filter(id=id).delete()
    return render(request, 'lanchonete/produtoDelete.html',context)

def historico(request, id=None):
    context = {**global_context, 'nome_do_usuario':'Thalles'}
    context['item_id'] = id
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
    transacoes = {
        'compra': Compra.objects.filter(user=UserTL(id=1)),
        'pagamentos': Pagamento.objects.filter(user=UserTL(id=1))
    }
    context = {**context_user, 'nome_do_usuario':'Thalles'}
    context = setPageActiveuser(context,'RainhaSaldoConsDetalhe')
    context['transacoes'] = transacoes

    if request.method=='GET':
        return render(request, 'lanchonete/RainhaSaldoConsDetalhe.html',context)

    elif request.method=='POST':
        form_data = request.POST.dict()
        print(form_data)
        if form_data.get('tipo_de_transacao') == 'tudo':
            transacoes = {
                Compra.objects.filter(user=UserTL(id=1)) , Pagamento.objects.filter(user=UserTL(id=1))
            }
            context['transacoes'] = transacoes

        if form_data.get('tipo_de_transacao') == 'compras':
            transacoes = {
                Compra.objects.filter(user=UserTL(id=1)),
            }
            context['transacoes'] = transacoes
        if form_data.get('tipo_de_transacao') == 'pagamentos':
            transacoes = {
                Pagamento.objects.filter(user=UserTL(id=1)),
            }
            context['transacoes'] = transacoes
        
        return render(request, 'lanchonete/RainhaSaldoConsDetalhe.html',context)
