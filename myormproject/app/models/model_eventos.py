from django.db import models

class Evento(models.Model):
    nome = models.CharField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    valor = models.FloatField()
    local = models.CharField()
    descricao = models.CharField()
    link_compra = models.URLField()
    link_validacao = models.URLField()
    