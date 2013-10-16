from quest.questao.subjetiva.models import QuestaoSubjetiva, RespostaSubjetiva
from quest.questao.forms import QuestaoForm
from tinymce import models as tinymce_models
from django import forms

class QuestaoSubjetivaForm(QuestaoForm):
    class Meta:
        model = QuestaoSubjetiva
        exclude = ['questionarios', 'criador', 'nivel_dinamico']
    def __init__(self, *args, **kwargs):
        super(QuestaoSubjetivaForm, self).__init__(*args, **kwargs)
        self.fields['resposta'] = forms.CharField(widget=forms.Textarea(attrs={'class':"cleditor", 'rows':7, 'cols':60}))

class RespostaSubjetivaForm(forms.ModelForm):
    class Meta:
        model = RespostaSubjetiva
        exclude = ["submissao", "questao"]
        
    def __init__(self, questao, *args, **kwargs):
        super(RespostaSubjetivaForm, self).__init__(*args, **kwargs)
        self.questao = questao
        self.fields['resposta'] = forms.CharField(widget=forms.Textarea(attrs={'class':"cleditor", 'rows':7, 'cols':60}))
        
QuestaoSubjetiva.RespostaForm = RespostaSubjetivaForm

