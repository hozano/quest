# coding:utf-8
from quest.questao.objetiva.models import QuestaoObjetiva, AlternativaQuestao,\
    RespostaObjetiva
from quest.questao.forms import QuestaoForm
from django.forms.formsets import formset_factory, BaseFormSet
from django import forms
import random

class QuestaoObjetivaForm(QuestaoForm):
    class Meta:
        model = QuestaoObjetiva
        exclude = ['questionarios', 'criador', 'nivel_dinamico']

class AlternativaObjetivaForm(forms.ModelForm):
    class Meta:
        model = AlternativaQuestao
        exclude = ['questao',]
        
    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = True)

class BaseAlternativaFormSet(BaseFormSet):
    
    def clean(self):
        if any(self.errors):
            return
        
        num_forms = 0
        valor_verdadeiro = 0
        for i in range(self.total_form_count()):
            form = self.forms[i]
            if form.cleaned_data and form.cleaned_data['alternativa']:
                num_forms += 1
                if form.cleaned_data['valor']:
                    valor_verdadeiro += 1
        if num_forms < 2:
            raise forms.ValidationError("Você deve indicar pelo menos 2 alternativas.")
        if valor_verdadeiro != 1 and self.form == AlternativaObjetivaForm:
            raise forms.ValidationError("Você deve indicar exatamente 1 alternativa verdadeira.")
        

AlternativaObjetivaFormSet = formset_factory(AlternativaObjetivaForm, formset=BaseAlternativaFormSet, extra=4, max_num=7)

class RespostaObjetivaForm(forms.ModelForm):
    class Meta:
        model = RespostaObjetiva
        exclude = ["questao", "submissao", "resposta"]
        
    def __init__(self, questao, *args, **kwargs):
        super(RespostaObjetivaForm, self).__init__(*args, **kwargs)
        self.questao = questao
        alternativas = [(alternativa.id, alternativa.alternativa) for alternativa in self.questao.alternativaquestao_set.all()]
        random.shuffle(alternativas)
        self.fields['alternativas'] = forms.TypedChoiceField(choices=alternativas,widget=forms.RadioSelect)
        
    def save(self, commit=True):
        resposta = super(RespostaObjetivaForm, self).save(commit)
        alternativa = self.cleaned_data["alternativas"]
        alternativa = self.questao.alternativaquestao_set.get(id = alternativa)
        resposta.resposta = alternativa.alternativa
        return resposta
               
QuestaoObjetiva.RespostaForm = RespostaObjetivaForm