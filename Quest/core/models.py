#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Professor(models.Model):
    user = models.OneToOneField(User)
        
    def __unicode__(self):
        return self.user.get_full_name()  
    
    def field_list(self):
        return [('Nome', self.user.get_full_name()), ('Email', self.email)]
    
    def get_questoes_criadas(self):
        items = []
        for cl in [name for name in dir(self.user) if name.startswith('questao')]:
            items += list(eval('self.user.%s.all()' % cl))
        return items
    
    def get_disciplinas(self):
        disc = []
        for disciplina in Disciplina.objects.all():
            if disciplina.professor == self.user.professor:
                disc.append(disciplina)
        return disc
    
    @property 
    def email(self):
        return self.user.email
    
    class Meta:
        permissions = (("professor", "permissao de professor"),)

class Aluno(models.Model):
    matricula = models.CharField(max_length= 15)
    user = models.OneToOneField(User)
    
    @property
    def nome(self):
        return self.user.get_full_name()
    
    def __unicode__(self):
        return self.user.get_full_name()  
    
    def field_list(self):
        return [('Matricula', self.matricula), ('Nome', self.nome), ('Email', self.user.email)]
    

class Disciplina(models.Model):
    alunos = models.ManyToManyField(Aluno)
    codigo = models.CharField(max_length = 10)
    nome = models.CharField(max_length = 30)
    professor = models.ForeignKey(Professor)
    
    def __unicode__(self):
        return self.codigo
    
    def field_list(self):
        return [('Codigo', self.codigo), ('Nome', self.nome), ('Professor', self.professor)]