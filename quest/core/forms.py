#-*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from quest.core.models import Aluno, Grupo
from django.contrib.auth.forms import UserCreationForm

class ProfessorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Um úsuario com este e-mail já existe.")

class AlunoForm(UserCreationForm):
    matricula = forms.CharField(max_length= 15, label="matricula")
    class Meta:
        model = User
        fields = ("matricula","username", "first_name", "last_name", "email")
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Um úsuario com este e-mail já existe.")
    
    
class AlunosForm(forms.Form):
    arquivo = forms.FileField()
    
class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        exclude = ["alunos", "professor", "questionarios"]
        
class GrupoAddAlunosForm(forms.Form):
        
    def __init__(self, disciplina, filtro, *args, **kwargs):
        super(GrupoAddAlunosForm, self).__init__(*args, **kwargs)
        matriculados = disciplina.alunos.all()
        disponiveis = [aluno for aluno in Aluno.objects.all() if aluno not in matriculados and filtro in aluno.nome]
        self.fields["alunos_disponiveis"] = forms.MultipleChoiceField(
                                choices=[('%d' % (aluno.id), "%s - %s" % (aluno.matricula, aluno)) for aluno in disponiveis])

    
#class QuestaoForm(forms.ModelForm):
#    enunciado = tinymce_models.HTMLField()
#    tags = forms.CharField()
#    
#class QuestaoSubjetivaForm(QuestaoForm):
#    class Meta:
#        model = QuestaoSubjetiva
#        
#class QuestaoObjetivaForm(QuestaoForm):
#    class Meta:
#        model = QuestaoObjetiva
#
#class QuestaoVFForm(QuestaoForm):
#    class Meta:
#        model = QuestaoVF
#
#class AlternativaObjetivaForm(forms.ModelForm):
#    class Meta:
#        model = AlternativaQuestao
#        exclude = ['questao',]
#        
#class AlternativaVFForm(forms.ModelForm):
#    class Meta:
#        model = AlternativaQuestao
#        exclude = ['questao',]
#        
#class BaseAlternativaFormSet(BaseFormSet):
#    
#    def clean(self):
#        if any(self.errors):
#            return
#        
#        num_forms = 0
#        valor_verdadeiro = 0
#        for i in range(self.total_form_count()):
#            form = self.forms[i]
#            if form.cleaned_data and form.cleaned_data['alternativa']:
#                num_forms += 1
#                if form.cleaned_data['valor']:
#                    valor_verdadeiro += 1
#        if num_forms < 2:
#            raise forms.ValidationError("Você deve indicar pelo menos 2 alternativas.")
#        if valor_verdadeiro != 1 and self.form == AlternativaObjetivaForm:
#            raise forms.ValidationError("Você deve indicar exatamente 1 alternativa verdadeira.")
#        
#            
#AlternativaObjetivaFormSet = formset_factory(AlternativaObjetivaForm, formset=BaseAlternativaFormSet, extra=4, max_num=7)
#AlternativaVFFormSet = formset_factory(AlternativaVFForm, formset=BaseAlternativaFormSet, extra=4, max_num=7)
#
#class SubmissaoForm(forms.ModelForm):
#    class Meta:
#        model = Submissao
#        exclude = ['data_hora', 'questionario']
#        
#class RespostaForm(forms.Form):
#    
#    RESPOSTA_CLASSES = {'Subjetiva':RespostaQSubjetiva, 'Objetiva':RespostaQObjetiva, 'V ou F':RespostaQVF}
#    
#    def __init__(self, questao, *args, **kwargs):
#        self.questao = questao.concrete()
#        super(RespostaForm, self).__init__(*args, **kwargs)
#        self.__create_fields()
#
#    def __create_fields(self):
#        if isinstance(self.questao, QuestaoSubjetiva):
#            self.fields['subjetiva'] = forms.CharField(widget=forms.Textarea(attrs={'rows':7, 'cols':80}))
#        elif isinstance(self.questao, QuestaoObjetiva):
#            alternativas = []
#            for alternativa in self.questao.alternativaquestao_set.all():
#                alternativas.append((alternativa.id, alternativa.alternativa))
#            self.fields['objetiva'] = forms.TypedChoiceField(choices=alternativas,widget=forms.RadioSelect)
#        elif isinstance(self.questao, QuestaoVF):
#            alternativas = []
#            for alternativa in self.questao.alternativaquestao_set.all():
#                self.fields['vf-%s' % alternativa.id] = forms.BooleanField(label=alternativa.alternativa, initial=False, required=False)
#    
#def make_forms_from_questionario(questionario, data=None):
#    forms = []
#    for questao in questionario.questoes.all():
#        forms.append(RespostaForm(questao, data=data, prefix='q%s' % questao.id))
#        
#    return forms
#
