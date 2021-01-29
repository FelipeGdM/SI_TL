from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserTL(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_rainha = models.BooleanField()

class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    valor = models.IntegerField()
    estoque = models.IntegerField()
    nome = models.CharField(max_length=64)
    def __str__(self):
        return self.nome

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=64)

    def __str__(self):
        return self.descricao

class Historico(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(Evento, on_delete=models.CASCADE)
    info = models.CharField(max_length=64)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.info

class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserTL, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    produtos = models.JSONField()
    valor = models.IntegerField()

class Pagamento(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserTL, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    valor = models.IntegerField()
    especie = models.BooleanField()

    def __str__(self):
        return f"{self.data} - {self.valor} TB"

class OpContabilRainha(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserTL, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    retirada_especie = models.IntegerField()
    retirada_online = models.IntegerField()

    def __str__(self):
        return f"{self.data} - {self.retirada_especie + self.retirada_online} TB"
