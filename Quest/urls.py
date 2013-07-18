# coding:utf-8
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from quest.core.models import Professor, Aluno, Disciplina
from django.views.generic import ListView, DetailView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.decorators import  permission_required, login_required
from quest.questao.models import Submissao
from django.contrib.auth.forms import AdminPasswordChangeForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    
    (r'^$', 'quest.core.views.index'),
    (r'^home$', 'quest.core.views.home'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'public/login.html'}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^cadastros$', 'quest.core.views.cadastro'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    (r'^mudar_pwd$', 'django.contrib.auth.views.password_change', {'password_change_form': AdminPasswordChangeForm, 'template_name' : 'private/professor/pwd.html'}),    
    (r'home$', 'django.contrib.auth.views.password_change_done', {'template_name' : 'private/home.html'}),
    
    (r'^professor$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Professor, template_name="private/professor/list.html"))),
    (r'^professor/list$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Professor, template_name="private/professor/list.html"))),
    (r'^professor/create$', 'quest.core.views.criar_professor'),
    (r'^professor/detail/(?P<pk>\d+)$', DetailView.as_view(model=Professor, template_name='private/professor/professor.html')),
    
    (r'^aluno$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Aluno, template_name="private/aluno/list.html"))),
    (r'^aluno/list$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Aluno, template_name="private/aluno/list.html"))),
    (r'^aluno/create$', 'quest.core.views.criar_aluno'),
    (r'^aluno/create_m$', 'quest.core.views.criar_alunos'),
    (r'^aluno/detail/(?P<pk>\d+)$', DetailView.as_view(model=Aluno, template_name='private/aluno/aluno.html')),
    
    (r'^disciplina/list$', permission_required("core.professor",login_url="/home")(ListView.as_view(model=Disciplina, template_name="private/disciplina/list.html"))),
    (r'^disciplina/create$', 'quest.core.views.criar_disciplina'),
    (r'^disciplina/detail/(?P<pk>\d+)$', DetailView.as_view(model=Disciplina, template_name='private/disciplina/disciplina.html')),
    (r'^disciplina/add/(?P<pk>\d+)$', 'quest.core.views.adicionar_alunos_disciplina'),
    
    (r'^questoes$', 'quest.questao.views.questoes'),
    (r'^questao/create/(?P<uid>[a-zA-Z_]\w*)$', 'quest.questao.views.criar_questao'),
    (r'^questao/detail/(?P<uid>[a-zA-Z_]\w*)/(?P<pk>\d+)/$', 'quest.questao.views.show_questao'),
    (r'^questao/deletar/(?P<uid>[a-zA-Z_]\w*)/(?P<pk>\d+)$', 'quest.questao.views.remover_questao'),
    (r'^questao/modificar/(?P<uid>[a-zA-Z_]\w*)/(?P<pk>\d+)$', 'quest.questao.views.atualizar_questao'),
    
    (r'^questionarios$', 'quest.questao.views.questionarios'),
    (r'^questionario/create$', 'quest.questao.views.criar_questionario'),
    (r'^questionario/detail/(?P<pk>\d+)$', 'quest.questao.views.show_questionario'),
    (r'^questionario/aplicar/(?P<pk>\d+)$', 'quest.questao.views.aplicar_questionario'),
    (r'^questionario/submeter/(?P<pk>\d+)$', 'quest.questao.views.submeter_questionario'),
    (r'^questionario/pontuar/(?P<pk>\d+)$', 'quest.questao.views.pontuar_questionario'),
    
    (r'^submissoes$', 'quest.questao.views.listar_submissoes'),
    (r'^submissoes/disciplina_(?P<disciplina_id>\d+)$', 'quest.questao.views.listar_submissoes'),
    (r'^submissoes/(?P<disciplina_id>\d+)/questionario_(?P<questionario_id>\d+)$', 'quest.questao.views.listar_submissoes'),
    (r'^submissoes/(?P<disciplina_id>\d+)/aluno_(?P<aluno_id>\d+)$', 'quest.questao.views.listar_submissoes'),
    (r'^submissoes/(?P<disciplina_id>\d+)/(?P<aluno_id>\d+)/questionario_(?P<questionario_id>\d+)$', 'quest.questao.views.listar_submissoes'),
    (r'^submissao/detail/(?P<pk>\d+)$', login_required(DetailView.as_view(model=Submissao, template_name="private/submissao/submissao.html"))),
    (r'^submissao/detail/(?P<pk>\d+)/(?P<disciplina>\d+)/(?P<aluno>\d+)$', login_required(DetailView.as_view(model=Submissao, template_name="private/submissao/submissao.html"))),
    (r'^submissoes/pontuar/(?P<pk>\d+)$', 'quest.questao.views.pontuar_submissao'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),

)

urlpatterns += staticfiles_urlpatterns()

#urlpatterns += create_crud_urls_from_models([Questao,])

