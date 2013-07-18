# coding:utf-8
from django.db import models
from quest.questao.models import Questao, Resposta

class QuestaoObjetiva(Questao):
    class Meta:
        app_label = 'questao'
    
    def get_tipo(self): return "Objetiva"
    
    def get_resposta(self):
        return AlternativaQuestao.objects.get(questao=self, valor=True)

class AlternativaQuestao(models.Model):
    questao = models.ForeignKey(QuestaoObjetiva)
    alternativa = models.CharField(max_length=200)
    valor = models.BooleanField()
    
    class Meta:
        app_label = 'questao'
        
    def __unicode__(self):
        return self.alternativa
    
class RespostaObjetiva(Resposta):
    questao = models.ForeignKey(QuestaoObjetiva)
    resposta = models.CharField(max_length=200)
    
    class Meta:
        app_label = "questao"
        
    def __unicode__(self):
        return self.resposta
