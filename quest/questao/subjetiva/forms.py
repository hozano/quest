from quest.questao.subjetiva.models import QuestaoSubjetiva, RespostaSubjetiva
from quest.questao.forms import QuestaoForm
from tinymce import models as tinymce_models
from django import forms

class QuestaoSubjetivaForm(QuestaoForm):
    resposta = tinymce_models.HTMLField()
    class Meta:
        model = QuestaoSubjetiva
        exclude = ['questionarios', 'criador', 'nivel_dinamico']
        

class RespostaSubjetivaForm(forms.ModelForm):
    resposta = tinymce_models.HTMLField()
    class Meta:
        model = RespostaSubjetiva
        exclude = ["submissao", "questao"]
        
    def __init__(self, questao, *args, **kwargs):
        super(RespostaSubjetivaForm, self).__init__(*args, **kwargs)
        self.questao = questao
        
QuestaoSubjetiva.RespostaForm = RespostaSubjetivaForm

