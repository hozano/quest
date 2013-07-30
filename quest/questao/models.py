# coding:utf-8
from django.contrib.auth.models import User 
from django.db import models
from quest import tagging
from quest.core.models import Disciplina, Aluno

class Questionario(models.Model):
    nome = models.CharField(max_length=100)
    criador = models.ForeignKey(User)
    disciplinas = models.ManyToManyField(Disciplina)
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()
    dicionario = {}
    
    def pontuar(self, lis):
        for i, j in enumerate(self.get_questoes()):
            self.dicionario[j] = lis[i]
        return self.dicionario
    
    def field_list(self):
        return [('Nome', self.nome), ('Data Início', self.hora_inicio), ('No. Questões', self.questoes.count())]
    
    @property
    def get_criador(self):
        return self.criador.get_full_name()
    
    def get_questoes(self):
        items = []
        for cl in [name for name in dir(self) if name.startswith('questao')]:
            qset = eval('self.%s.all()' % cl)
            [items.append(item) for item in qset]
        return items
    
    def get_tags(self):
        tags = []
        for questao in self.get_questoes():
            tags.extend(questao.get_tags())
        return set(tags)
    
    def get_tags_as_string(self):
        string_tags = [tag.name for tag in self.get_tags()]
        return ", ".join(string_tags)
    
    def __unicode__(self):
        return self.nome

class QuestaoManager(models.Manager):pass

class Questao (models.Model):
    
    nome = models.CharField(max_length=100)
    enunciado = models.TextField()
    criador = models.ForeignKey(User)
    data_criacao = models.DateTimeField(auto_now_add=True)
    nivel_estatico = models.IntegerField()
    nivel_dinamico = models.IntegerField(null=True)
    questionarios = models.ManyToManyField(Questionario)
    
    objects = QuestaoManager()
    
    class Meta:
        abstract = True
        
    def __unicode__(self): return self.nome
    
    @property
    def get_criador(self):
        return self.criador.get_full_name()

    def uid(self): return self.__module__.split('.')[-2]
    
    def modulo(self): return modulo_map[self.uid()]
    
    def get_tags(self): return self.tags
    
    def get_tags_as_string(self):
        string_tags = [tag.name for tag in self.get_tags()]
        return ", ".join(string_tags)
    
    def field_list(self):
        return [('Nome', self.nome), ('Tags', self.get_tags_as_string()),]
    
    def get_respostaForm(self, **kwargs):
        return self.RespostaForm(self, **kwargs)
    
tagging.register(Questao)

class Submissao(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    questionario = models.ForeignKey(Questionario)
    aluno = models.ForeignKey(Aluno)
    nota = models.IntegerField(null=True)
    
    def field_list(self):
        return [('Questionário', self.questionario), ('Hora', self.data_hora)]
    
    def get_respostas(self):
        items = []
        for cl in [name for name in dir(self) if name.startswith('resposta')]:
            qset = eval('self.%s.all()' % cl)
            [items.append(item) for item in qset]
        return items
    
    def __unicode__(self):
        return "submissao para %s" % self.questionario
    
class Resposta(models.Model):
    submissao = models.ForeignKey(Submissao)
    class Meta:
        abstract = True
        
import os, sys
QUESTOES_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, QUESTOES_PATH)

def import_libs(caminho):
    """ Imports the libs, returns a list of the libraries. 
    Pass in dir to scan """
       
    library_list = []
    
    for f in os.listdir(os.path.abspath(caminho)):
        module_name, ext = os.path.splitext(f) # Handles no-extension files, etc.
        excluded_modules = ['models', 'views', '__init__', 'admin', 'forms', 'sql']
        
        ''' Modificado: ext == '.py' para ext != '.pyc', afim de importar também os diretórios filhos.'''
        if module_name and ext != '.pyc' and module_name not in excluded_modules: # Important, ignore .pyc/other files.
            print "Importando modulos: %s" % module_name
            module = __import__(module_name)
            library_list.append(module)
 
    return library_list

modulos = import_libs(QUESTOES_PATH)
modulo_map = {}
for modulo in modulos:
    modulo_map[modulo.uid] = modulo

def get_questoes():
    questoes = []
    for modulo in modulos:
        questoes.extend(modulo.classe.objects.all())
    return questoes
