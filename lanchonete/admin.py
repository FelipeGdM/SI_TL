from django.contrib import admin

# Register your models here.
from .models import Produto, Evento, Historico, Compra, Pagamento, OpContabilRainha, UserTL

admin.site.register(Produto)
admin.site.register(Evento)
admin.site.register(Historico)
admin.site.register(Compra)
admin.site.register(Pagamento)
admin.site.register(OpContabilRainha)
admin.site.register(UserTL)
