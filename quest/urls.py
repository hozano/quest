# coding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.models import Professor, Aluno, Grupo
from django.views.generic import ListView, DetailView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.decorators import  permission_required, login_required
from questao.models import Submissao
from django.contrib.auth.forms import AdminPasswordChangeForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    
    (r'^$', 'core.views.index'),
    (r'^home$', 'core.views.home'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'public/login.html'}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^cadastros$', 'core.views.cadastro'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    (r'^mudar_pwd$', 'core.views.pass_change'),    
    (r'home$', 'django.contrib.auth.views.password_change_done', {'template_name' : 'private/home.html'}),
    
    (r'^professor$',  'core.views.professor'),
    (r'^professor/list$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Professor, template_name="private/professor/list.html"))),
    (r'^professor/create$', 'core.views.criar_professor'),
    (r'^professor/detail/(?P<pk>\d+)$', DetailView.as_view(model=Professor, template_name='private/professor/professor.html')),
    
    (r'^aluno$', 'core.views.aluno'),
    (r'^aluno/list$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Aluno, template_name="private/aluno/list.html"))),
    (r'^aluno/create$', 'core.views.criar_aluno'),
    (r'^aluno/create_m$', 'core.views.criar_alunos'),
    (r'^aluno/detail/(?P<pk>\d+)$', DetailView.as_view(model=Aluno, template_name='private/aluno/aluno.html')),
    
    (r'^grupo$', 'core.views.grupo'),
    (r'^grupo/list$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Grupo, template_name="private/disciplina/list.html"))),
    (r'^grupo/create$', 'core.views.criar_grupo'),
    (r'^grupo/detail/(?P<pk>\d+)$',  'core.views.show_grupo'),
    (r'^grupo/add/(?P<pk>\d+)$', 'core.views.adicionar_alunos_grupo'),
    
    (r'^questoes$', 'questao.views.questoes'),
    (r'^questao/create/(?P<uid>[a-zA-Z_]\w*)$', 'questao.views.criar_questao'),
    (r'^questao/detail/(?P<uid>[a-zA-Z_]\w*)/(?P<pk>\d+)/$', 'questao.views.show_questao'),
    (r'^questao/deletar/(?P<uid>[a-zA-Z_]\w*)/(?P<pk>\d+)$', 'questao.views.remover_questao'),
    (r'^questao/modificar/(?P<uid>[a-zA-Z_]\w*)/(?P<pk>\d+)$', 'questao.views.atualizar_questao'),
    
    (r'^questionarios$', 'questao.views.questionarios'),
    (r'^questionario/create$', 'questao.views.criar_questionario'),
    (r'^questionario/detail/(?P<pk>\d+)$', 'questao.views.show_questionario'),
    (r'^questionario/delete/(?P<pk>\d+)$', 'questao.views.delete_questionario'),
    (r'^questionario/aplicar/(?P<pk>\d+)$', 'questao.views.aplicar_questionario'),
    (r'^questionario/submeter/(?P<pk>\d+)$', 'questao.views.submeter_questionario'),
    (r'^questionario/pontuar/(?P<pk>\d+)$', 'questao.views.pontuar_questionario'),
    
    (r'^submissoes$', 'questao.views.submissao'),
    (r'^submissao/detail/(?P<pk>\d+)$', login_required(DetailView.as_view(model=Submissao, template_name="private/submissao/submissao.html"))),
    (r'^submissoes/pontuar/(?P<pk>\d+)$', 'questao.views.pontuar_submissao'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^tinymce/', include('tinymce.urls')),

)

urlpatterns += staticfiles_urlpatterns()

#urlpatterns += create_crud_urls_from_models([Questao,])

