#coding:utf-8
from models import QuestaoObjetiva
from forms import QuestaoObjetivaForm, AlternativaObjetivaFormSet
from views import criar_questao, show_questao, atualizar_questao, remover_questao

uid = 'objetiva'
tipo_string = 'Questão Objetiva'
classe = QuestaoObjetiva
form = QuestaoObjetivaForm
formset = AlternativaObjetivaFormSet
