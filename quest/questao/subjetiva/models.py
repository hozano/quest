# coding:utf-8
from django.db import models
from questao.models import Questao, Resposta

class QuestaoSubjetiva(Questao):
    resposta = models.TextField()
    
    class Meta:
        app_label = 'questao'
        
    def get_tipo(self): return "Subjetiva"
    
    def get_resposta(self):
        return self.resposta
    

class RespostaSubjetiva(Resposta):
    resposta = models.TextField()
    questao = models.ForeignKey(QuestaoSubjetiva)
    class Meta:
        app_label = 'questao'
    
    def __unicode__(self):
        return self.resposta
    