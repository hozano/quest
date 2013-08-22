#coding:utf-8
from models import QuestaoSubjetiva
from forms import QuestaoSubjetivaForm
from views import criar_questao, show_questao,atualizar_questao ,remover_questao

uid = 'subjetiva'
tipo_string = 'Questão Subjetiva'
classe = QuestaoSubjetiva
form = QuestaoSubjetivaForm

