#coding:utf-8
from quest.questao.objetiva.models import QuestaoObjetiva
from quest.questao.objetiva.forms import QuestaoObjetivaForm, AlternativaObjetivaFormSet
from quest.questao.objetiva.views import criar_questao, show_questao,atualizar_questao ,remover_questao

uid = 'objetiva'
tipo_string = 'Questão Objetiva'
classe = QuestaoObjetiva
form = QuestaoObjetivaForm
formset = AlternativaObjetivaFormSet
