from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import F
from .utils import setPageActive
from .utils import setPageActiveuser
from .utils import calculaSaldoConsumidor
from .utils import calculaSaldoTotal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Produto, Compra, UserTL,Pagamento, Evento, TipoEvento
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

sidebar_pages = [
    {
        'name': 'Dashboard',
        'icon': 'home',
        'active': False,
        'link': '/rainhaHome'
    },
    {
        'name': 'Saldo consumidores',
        'icon': 'users',
        'active': False,
        'link': '/rainhaSaldoCons'
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

def index(request):
    if 'user_id' in request.session:
        return redirect('homeuser')
    else:
        return redirect('signin')

def dashboard(request):
    return HttpResponse('Dashboard')

def signin(request):
    
    if request.method=='GET':
        return render(request, 'lanchonete/signin.html')
    
    elif request.method=='POST':
    
        form_data = request.POST.dict()
        usuario_logado = authenticate(request,username=form_data['username'], password=form_data['password'])
       
        if usuario_logado is not None:
            if usuario_logado.is_active:
                login(request, usuario_logado)
                user = UserTL.objects.filter(user=request.user).first()
                if user.is_rainha:
                    return redirect('rainhaHome')
                else:
                    return redirect('homeuser')

        return HttpResponse('Usuário ou Senha inválidos')

    else:
        return HttpResponse('Unsupported method!')

def register(request):
    if request.method=='GET':
        return render(request, 'lanchonete/register.html') 
    elif request.method=='POST':
        form_data = request.POST.dict()
        user = User.objects.create_user(username=form_data['first_name']+form_data['last_name'], first_name=form_data['first_name'] ,email=form_data['email'] ,password=form_data['password_confirmation'])
        UserTL.objects.create(user=user, is_rainha=False)
        return redirect('signin') 

def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required
def homeuser(request):
    user = UserTL.objects.filter(user=request.user).first()
    transacoes = [*list(Compra.objects.filter(user=user)),*list(Pagamento.objects.filter(user=user))]
    context = {**context_user, 'nome_do_usuario':request.user.first_name}
    context = setPageActiveuser(context,'homeuser')
    context['saldo_do_usuario'] = calculaSaldoConsumidor(user)
    context['transacoes'] = transacoes
    if request.method=='GET':
        return render(request, 'lanchonete/homeuser.html',context)

    elif request.method=='POST':
        form_data = request.POST.dict()
        if form_data.get('tipo_de_transacao') == 'tudo':
            transacoes = [*list(Compra.objects.filter(user=user)),*list(Pagamento.objects.filter(user=user))]
            context['transacoes'] = transacoes

        if form_data.get('tipo_de_transacao') == 'compras':
            transacoes = Compra.objects.filter(user=user)
            context['transacoes'] = transacoes

        if form_data.get('tipo_de_transacao') == 'pagamentos':
            transacoes = Pagamento.objects.filter(user=user)
            context['transacoes'] = transacoes
        
        context['form_data'] = form_data
        return render(request, 'lanchonete/homeuser.html',context)

        #maracutaias legais

@login_required
def pagamento(request):
    user = UserTL.objects.filter(user=request.user).first()
    context = {**context_user, 'nome_do_usuario':request.user.first_name}
    context = setPageActiveuser(context,'pagamento')
    if request.method=='GET':
        return render(request, 'lanchonete/pagamento.html',context)

    elif request.method=='POST':
        form_data = request.POST.dict()
        context['pagamento_feito'] = False
        if form_data['forma_de_pagamento'] != '' and form_data['quantia_paga']!= '0':
            context['pagamento_feito'] = True
            Pagamento.objects.create(user=user,especie=form_data['forma_de_pagamento'] , valor=form_data['quantia_paga'])     
            Evento.objects.create(info=f'Pagou {form_data["quantia_paga"]}TBs', tipo='Pagamento')

        return render(request, 'lanchonete/pagamento.html',context)

@login_required    
def carrinho(request):
    user = UserTL.objects.filter(user=request.user).first()
    produto = {
        'salgado': Produto.objects.filter(tipo='salgado', disponivel=True),
        'doce': Produto.objects.filter(tipo='doce', disponivel=True ),
        'bebida': Produto.objects.filter(tipo='bebida', disponivel=True),
    }
    context = {**context_user, 'nome_do_usuario':request.user.first_name, 'produtos': produto}
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

            Compra.objects.create(user=user, produtos=produtos, valor=valor_compra)
            context['compra_finalizada'] = True
            return render(request, 'lanchonete/carrinho.html', context)
        else:

            context['compra_finalizada'] = False
            context['compra_erro'] = True
            return render(request, 'lanchonete/carrinho.html', context)

    else:
        return HttpResponse('Requisição inválida!')

@login_required
def estoque(request):
    user = UserTL.objects.filter(user=request.user).first()
    if not user.is_rainha:
        return redirect('homeuser')
    produto = {
        'salgado': Produto.objects.filter(tipo='salgado', disponivel=True),
        'doce': Produto.objects.filter(tipo='doce', disponivel=True),
        'bebida': Produto.objects.filter(tipo='bebida', disponivel=True),
    }
    context = {**global_context, 'nome_do_usuario':request.user.first_name, 'produtos': produto}
    context = setPageActive(context,'estoque')
    context['listagem_produtos'] = [*list(produto["salgado"]), *list(produto["doce"]), *list(produto["bebida"])]
    
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

@login_required
def inventario(request):
    user = UserTL.objects.filter(user=request.user).first()
    if not user.is_rainha:
        return redirect('homeuser')    
    user = UserTL.objects.filter(user=request.user).first()
    produto = {
        'salgado': Produto.objects.filter(tipo='salgado'),
        'doce': Produto.objects.filter(tipo='doce'),
        'bebida': Produto.objects.filter(tipo='bebida'),
    }
    context = {**global_context, 'nome_do_usuario':request.user.first_name, 'produtos': produto}
    context = setPageActive(context,'inventario')
    context['item_adicionado'] = False
    context['listagem_produtos'] = [*list(produto["salgado"]), *list(produto["doce"]), *list(produto["bebida"])]

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
        
        elif form_data['nome_do_formulario'] == "formulario_alterar_inventario":
            
            if form_data['disponibilidade'] != Produto.objects.filter(id=form_data['item_id']).get().disponivel:
                print("lalala")
                print(form_data['item_id'])
                Produto.objects.filter(id=form_data['item_id']).update(disponivel=form_data['disponibilidade'])

            if form_data['nome_editar'] != Produto.objects.filter(id=form_data['item_id']).get().nome:
                Produto.objects.filter(id=form_data['item_id']).update(nome=form_data['nome_editar'])

            if form_data['preco_editar'] != Produto.objects.filter(id=form_data['item_id']).get().valor:
                Produto.objects.filter(id=form_data['item_id']).update(valor=form_data['preco_editar'])

            if form_data['estoque_editar'] != Produto.objects.filter(id=form_data['item_id']).get().estoque:
                print("lalala")
                Produto.objects.filter(id=form_data['item_id']).update(estoque=form_data['estoque_editar'])   

        return render(request, 'lanchonete/inventario.html',context)
    
    else:
        return HttpResponse('Requisição inválida!')

@login_required
def produtoDelete(request, id=None):
    user = UserTL.objects.filter(user=request.user).first()
    if not user.is_rainha:
        return redirect('homeuser')
    context = {**global_context, 'nome_do_usuario':request.user.first_name}
    context['id'] = id
    Produto.objects.filter(id=id).delete()
    return render(request, 'lanchonete/produtoDelete.html',context)

@login_required
def historico(request, id=None):
    user = UserTL.objects.filter(user=request.user).first()
    if not user.is_rainha:
        return redirect('homeuser')
    context = {**global_context, 'nome_do_usuario':request.user.first_name}
    context['item_id'] = id
    return render(request, 'lanchonete/historico.html',context)

@login_required
def rainhaHome(request):
    user = UserTL.objects.filter(user=request.user).first()
    if not user.is_rainha:
        return redirect('homeuser')
    context = {**global_context, 'nome_de_usuario':request.user.first_name}
    pagamentos_em_especie = Pagamento.objects.filter(especie=True)
    pagamentos_em_cartao = Pagamento.objects.filter(especie=False)

    eventos = Evento.objects.filter()

    disponivel_em_especie = 0
    disponivel_em_cartao = 0 
    disponivel_total = 0
    balanco_consumidores = calculaSaldoTotal()
    
    for paga in pagamentos_em_especie:
        disponivel_em_especie += paga.valor

    for paga in pagamentos_em_cartao:
        disponivel_em_cartao += paga.valor

    disponivel_total = disponivel_em_cartao + disponivel_em_especie

    context = setPageActive(context, 'rainhaHome')
    context['disponivel_em_especie'] = disponivel_em_especie
    context['disponivel_em_cartao'] = disponivel_em_cartao
    context['disponivel_total'] = disponivel_total
    context['balanco_consumidores'] = balanco_consumidores
    context['eventos'] = eventos
    context['retirada_sucesso'] = False
    

    if request.method=='GET':
        return render(request, 'lanchonete/rainhaHome.html',context)
    elif request.method =='POST':
        form_data = request.POST.dict()
        disponivel_em_especie -= int(form_data['especie_retirado'])
        disponivel_em_cartao -= int(form_data['cartao_retirado'])

        disponivel_total = disponivel_em_cartao + disponivel_em_especie
        context['disponivel_em_especie'] = disponivel_em_especie
        context['disponivel_em_cartao'] = disponivel_em_cartao
        context['disponivel_total'] = disponivel_total
        context['balanco_consumidores'] = balanco_consumidores
        context['eventos'] = eventos
        context['retirada_sucesso'] = True

        if form_data['especie_retirado'] != '0':
            Pagamento.objects.create(user=user,especie=True, valor=-1*int(form_data['especie_retirado']))
            Evento.objects.create(info=f' Rainha retirou { form_data["especie_retirado"] } do saldo em espécie', tipo="Retirada")
        if form_data['cartao_retirado'] != '0':
            Pagamento.objects.create(user=user,especie=False, valor=-1*int(form_data['cartao_retirado']))
            Evento.objects.create(info=f' Rainha retirou { form_data["cartao_retirado"] } do saldo em cartão', tipo="Retirada")
        return render(request, 'lanchonete/rainhaHome.html',context)

@login_required
def rainhaSaldoCons(request):
    usuarios_tl = UserTL.objects.filter(is_rainha=False)
    usuarios = []
    for usuario in usuarios_tl:
        usuarios.append({
            'user': usuario.user,
            'saldo': calculaSaldoConsumidor(usuario),
        })
    user = UserTL.objects.filter(user=request.user).first()
    if not user.is_rainha:
        return redirect('homeuser')
    context = {**global_context, 'nome_do_usuario':request.user.first_name}
    context = setPageActive(context,'rainhaSaldoCons')
    context['usuarios'] = usuarios
    return render(request, 'lanchonete/rainhaSaldoCons.html',context)

@login_required
def rainhaSaldoConsDetalhe(request, id=None):
    user = UserTL.objects.filter(user=request.user).first()
    if not user.is_rainha:
        return redirect('homeuser')
    transacoes = {
        'compra': Compra.objects.filter(user=user),
        'pagamentos': Pagamento.objects.filter(user=user)
    }
    context = {**context_user, 'nome_do_usuario':request.user.first_name}
    context = setPageActiveuser(context,'rainhaSaldoConsDetalhe')
    context['transacoes'] = transacoes

    if request.method=='GET':
        return render(request, 'lanchonete/rainhaSaldoConsDetalhe.html',context)

    elif request.method=='POST':
        form_data = request.POST.dict()
        print(form_data)
        if form_data.get('tipo_de_transacao') == 'tudo':
            transacoes = {
                Compra.objects.filter(user=user) , Pagamento.objects.filter(user=user)
            }
            context['transacoes'] = transacoes

        if form_data.get('tipo_de_transacao') == 'compras':
            transacoes = {
                Compra.objects.filter(user=user),
            }
            context['transacoes'] = transacoes
        if form_data.get('tipo_de_transacao') == 'pagamentos':
            transacoes = {
                Pagamento.objects.filter(user=user),
            }
            context['transacoes'] = transacoes
        
        return render(request, 'lanchonete/rainhaSaldoConsDetalhe.html',context)