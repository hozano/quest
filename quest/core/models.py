#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Professor(models.Model):
    user = models.OneToOneField(User)
    about = models.TextField()
        
    def __unicode__(self):
        return self.user.get_full_name()  
    
    def field_list(self):
        return [('Nome', self.user.get_full_name()), ('Email', self.email)]
    
    def get_questoes_criadas(self):
        items = []
        for cl in [name for name in dir(self.user) if name.startswith('questao')]:
            items += list(eval('self.user.%s.all()' % cl))
        return items
    
    def get_grupos(self):
        return Grupo.objects.filter(professor = self)
    
    def email(self):
        return self.user.email
    
    class Meta:
        permissions = (("professor", "permissao de professor"),)

class Aluno(models.Model):
    matricula = models.CharField(max_length= 15)
    user = models.OneToOneField(User)
    about = models.TextField()
    
    def nome(self):
        return self.user.get_full_name()
    
    def get_grupos(self):
        return Grupo.objects.filter(alunos = self)
    
    def __unicode__(self):
        return self.user.get_full_name()  
    
    def field_list(self):
        return [('Matricula', self.matricula), ('Nome', self.nome), ('Email', self.user.email)]
    

class Grupo(models.Model):
    alunos = models.ManyToManyField(Aluno)
    codigo = models.CharField(max_length = 10)
    nome = models.CharField(max_length = 30)
    professor = models.ForeignKey(Professor)
    about = models.TextField()
    
    def __unicode__(self):
        return self.codigo
    
    def field_list(self):
        return [('Codigo', self.codigo), ('Nome', self.nome), ('Professor', self.professor)]
    
    def matriculados(self):
        return len(self.alunos.all())