# coding:utf-8
from models import QuestaoVF, AlternativaVFQuestao, RespostaVF
from questao.forms import QuestaoForm
from django.forms.formsets import formset_factory, BaseFormSet
from django import forms
import random

class QuestaoVFForm(QuestaoForm):
    class Meta:
        model = QuestaoVF
        exclude = ['questionarios', 'criador', 'nivel_dinamico']

class AlternativaVFForm(forms.ModelForm):
    class Meta:
        model = AlternativaVFQuestao
        exclude = ['questao',]

class BaseAlternativaFormSet(BaseFormSet):
    
    def clean(self):
        if any(self.errors):
            return
        
        num_forms = 0
        for i in range(self.total_form_count()):
            form = self.forms[i]
            if form.cleaned_data and form.cleaned_data['alternativa']:
                num_forms += 1
        if num_forms < 2:
            raise forms.ValidationError("Você deve indicar pelo menos 2 alternativas.")
        

AlternativaVFFormSet = formset_factory(AlternativaVFForm, formset=BaseAlternativaFormSet, extra=4, max_num=7)

class RespostaVFForm(forms.ModelForm):
    
    class Meta:
        model = RespostaVF
        exclude = ["submissao", "questao", "resposta"]
         
    def __init__(self, questao, *args, **kwargs):
        kwargs['label_suffix'] = ""
        super(RespostaVFForm, self).__init__(*args, **kwargs)
        self.questao = questao
        alternativas = list(self.questao.alternativavfquestao_set.all())
        random.shuffle(alternativas)
        for alternativa in alternativas:
            self.fields['vf-%s' % alternativa.id] = forms.BooleanField(label=unicode(alternativa.alternativa), initial=False, required=False)
            
    def save(self, commit = True):
        obj = super(RespostaVFForm, self).save(commit)
        resposta = ""
        alternativas = self.questao.alternativavfquestao_set.all()
        for alternativa in alternativas:
            resposta += "(%s) : %s;" % (self.cleaned_data["vf-%s" % alternativa.id], alternativa.alternativa)
        obj.resposta = resposta
        return obj
            
    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = u'<tr%(html_class_attr)s><td>%(field)s</td><td>%(errors)s <span>%(label)s</span> %(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="3">%s</td></tr>',
            row_ender = u'</td></tr>',
            help_text_html = u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row = True)
            
QuestaoVF.RespostaForm = RespostaVFForm
