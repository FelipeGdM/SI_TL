from django.contrib import admin

# Register your models here.
from .models import Produto, TipoEvento, Evento, Compra, Pagamento, OpContabilRainha, UserTL

admin.site.register(Produto)
admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(Compra)
admin.site.register(Pagamento)
admin.site.register(OpContabilRainha)
admin.site.register(UserTL)
