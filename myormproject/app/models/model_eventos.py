from django.db import models


class Evento(models.Model):
    id = models.CharField(primary_key=True, 
                          unique=True, 
                          editable=False,
                          max_length=50,)
    
    nome = models.CharField(max_length=500)
    data_inicio = models.CharField(max_length=500)
    data_fim = models.CharField(max_length=500)
    valor = models.CharField(max_length=500)
    local = models.CharField(max_length=500)
    descricao = models.TextField()
    link_validacao = models.TextField()
    url_imagem = models.TextField()

    is_deleted = models.BooleanField(default=False)
