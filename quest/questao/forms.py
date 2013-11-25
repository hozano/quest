# encoding:utf-8
from django import forms
from models import Questao, Questionario, Submissao
import random


class QuestaoForm(forms.ModelForm):
    nivel_estatico = forms.ChoiceField(choices=[(i,i) for i in range(1,11)])
    tags = forms.CharField()
    class Meta:
        model = Questao
        exclude = ['questionarios', 'criador', 'nivel_dinamico']
    def __init__(self, *args, **kwargs):
        super(QuestaoForm, self).__init__(*args, **kwargs)
        self.fields['enunciado'] = forms.CharField(widget=forms.Textarea(attrs={'class':"cleditor", 'rows':7, 'cols':60}))
        
        

class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        exclude = ['criador', 'disciplinas', 'grupos']
    
    def clean_hora_fim(self):
        inicio = self.cleaned_data["hora_inicio"]
        fim = self.cleaned_data["hora_fim"]
       
        if inicio < fim:
            return fim
        else:
            raise forms.ValidationError("O formulario deve finalizar depois da data inicial.")
        
    def __init__(self, *args, **kwargs):
        from models import get_questoes
        super(QuestionarioForm,self).__init__(*args,**kwargs)
        self.fields['questoes'] = forms.MultipleChoiceField(choices=[('%s#%d' % (i.uid(), i.id), '%s (%s)' % (i.nome, i.get_tags_as_string()) ) for i in get_questoes()],widget=forms.CheckboxSelectMultiple)    
        
class AplicarQuestionarioForm(forms.Form):
    def __init__(self, grupos, *args, **kwargs):
        super(AplicarQuestionarioForm, self).__init__(*args, **kwargs)
        self.fields['grupos'] = forms.MultipleChoiceField(choices=[(i.id, ("%s %s") % (i, i.nome)) for i in grupos])
        
class SubmissaoForm(forms.ModelForm):
    class Meta:
        model = Submissao
        exclude = ["questionario", "aluno"]
            
class RespostaForm(forms.Form):
    def __init__(self, questao, *args, **kwargs):
        super(RespostaForm, self).__init__(*args, **kwargs)
        self.questao = questao
        self.fields['resposta'] = forms.CharField(widget=forms.Textarea(attrs={'class':"cleditor", 'rows':7, 'cols':60}))
        
Questao.RespostaForm = RespostaForm

def make_forms_from_questionario(questionario, data=None):
    forms = []
    questoes = questionario.get_questoes()
    random.shuffle(questoes)
    for questao in questoes:
        forms.append(questao.get_respostaForm(data=data, prefix='q%s' % questao.id))
    return forms

