#coding:utf-8
from models import QuestaoVF
from forms import QuestaoVFForm, AlternativaVFFormSet
from views import criar_questao, show_questao, atualizar_questao ,remover_questao

uid = 'vf'
tipo_string = 'Questão V ou F'
classe = QuestaoVF
form =  QuestaoVFForm
formset = AlternativaVFFormSet