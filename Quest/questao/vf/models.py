#coding:utf-8
from django.db import models
from quest.questao.models import Questao, Resposta

class QuestaoVF(Questao):
    class Meta:
        app_label = 'questao'
        
    def get_resposta(self):
        alternativas =  AlternativaVFQuestao.objects.filter(questao=self)
        res = ""
        for alternativa in alternativas:
            res += "(%s) : %s " % (alternativa.valor, alternativa.alternativa)
            res += unicode("<br>")
        return  res

    def get_tipo(self): return "V ou F"

class AlternativaVFQuestao(models.Model):
    questao = models.ForeignKey(QuestaoVF)
    alternativa = models.CharField(max_length=200)
    valor = models.BooleanField()
    
    class Meta:
        app_label = 'questao'
     
    def __unicode__(self):
        return "(%s) : %s " %(self.valor, self.alternativa)

class RespostaVF(Resposta):
    questao = models.ForeignKey(QuestaoVF)
    resposta = models.CharField(max_length=200)
    
    class Meta:
        app_label = "questao"
        
    def __unicode__(self):
        res = self.resposta.split(";")
        result = ""
        for s in res:
            result += s+unicode("<br>")
        return result[:-4]