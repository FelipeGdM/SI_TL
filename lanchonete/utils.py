
from .models import Pagamento, Compra, UserTL

def setPageActive(context, page_name):
  for n, page in enumerate(context['sidebar_pages']):
      if page['link'][1:] == page_name:
        context['sidebar_pages'][n]['active'] = True
      else:
        context['sidebar_pages'][n]['active'] = False
  return context

def setPageActiveuser(context, page_name):
  for n, page in enumerate(context['sidebar_pages_user']):
      if page['link'][1:] == page_name:
        context['sidebar_pages_user'][n]['active'] = True
      else:
        context['sidebar_pages_user'][n]['active'] = False  
  return context

def calculaSaldoConsumidor(usuario_id):
  #Filtra as Compras e Pagamentos associados a um usuário
  compras = Compra.objects.filter(user=UserTL(id=usuario_id))
  pagamentos = Pagamento.objects.filter(user=UserTL(id=usuario_id))
  total_pago = 0
  total_comprado = 0
  #Calcula o valor total associados a compras:
  for compra in compras:
      total_comprado += compra.valor

  # Calcula o valor total de pagamentos:
  for val in pagamentos:
    total_pago += val.valor
  return total_pago - total_comprado

def calculaSaldoTotal():
  usuarios = UserTL.objects.filter(is_rainha= False ).values('id')
  saldo_total = 0 
  for usuario in usuarios:
    saldo_total += calculaSaldoConsumidor(usuario)
  
  return saldo_total
