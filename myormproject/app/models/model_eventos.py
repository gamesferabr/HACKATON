from django.db import models

class Evento(models.Model):
    nome = models.CharField(max_length=500)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    valor = models.FloatField()
    local = models.CharField(max_length=500)
    descricao = models.TextField()
    link_compra = models.URLField()
    link_validacao = models.URLField()
    