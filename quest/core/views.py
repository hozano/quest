#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.db.models import Q
from quest.core.models import Professor, Aluno, Grupo
from quest.core.forms import ProfessorForm, AlunoForm, GrupoForm,\
    GrupoAddAlunosForm, AlunosForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, User
from django.utils import simplejson


def index(request):
    '''Redireciona para a página principal.
    
    @param request: Requisição
    @type request: HttpRequest
    @return: Página principal
    @rtype: HttpResponse
    '''
    if request.user.is_authenticated(): return HttpResponseRedirect("/home")
    
    return render_to_response('public/index.html', context_instance=RequestContext(request))

@login_required
def home(request):
    '''Redireciona para a página principal.
    
    @param request: Requisição
    @type request: HttpRequest
    @return: Página principal
    @rtype: HttpResponse
    '''
    if request.user.has_perm("core.professor"):
        return render_to_response('private/index.html', context_instance=RequestContext(request))
    return render_to_response('private/aluno/index.html', context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def cadastro(request):
    '''Redireciona para a página principal.
    
    @param request: Requisição
    @type request: HttpRequest
    @return: Página principal
    @rtype: HttpResponse
    '''
    return render_to_response('private/cadastros.html', context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def criar_professor(request):
    print "criando professor"
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            with transaction.commit_on_success():
                user = form.save()
                user.user_permissions.add(Permission.objects.get(codename = "professor"))
                professor = Professor(user = user)
                professor.save()
                return HttpResponseRedirect('/professor')
    print "redirecionando"
    return HttpResponseRedirect('/professor')
    
@permission_required("core.professor", login_url="/home")
def professor(request):
    objects_list = Professor.objects.all()
    form = ProfessorForm()
    return render_to_response('private/professor/list.html', {'object_list': objects_list, 'form':form}, context_instance=RequestContext(request))
    

@permission_required("core.professor", login_url="/home")
def criar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            with transaction.commit_on_success():
                user = form.save()
                aluno = Aluno(matricula = form.cleaned_data['matricula'] ,user = user)
                aluno.save()
                return HttpResponseRedirect('/aluno')
    return HttpResponseRedirect('/aluno')

def get_alunos(request):
    alunos = Aluno.objects.all()
    if request.method == 'GET':
        if request.GET.has_key(u'term'):
            nome = request.GET[u'term']
            alunos = [aluno for aluno in alunos if aluno.nome.rfind(nome) == 0]
            res = [ (l.nome + ' ('+l.matricula+')') for l in alunos ]
            #return HttpResponse(simplejson.dumps(res), mimetype="application/x-javascript")
            #res = serializers.serialize("json", res)
            return HttpResponse(simplejson.dumps(res), mimetype="application/json")
        else:
            #Acessível por URL:/ajax
            alunos = Aluno.objects.all()
            res = [ (l.nome + ' ('+l.matricula+')') for l in alunos ]
            return HttpResponse(simplejson.dumps(res), mimetype="application/json") 

    if request.method=='POST':
        print "é post"
        nome = request.POST[u'term']
        a = nome.split('(').__str__()
        print a
        b = a[-1].split(')')
        print b
        pk = b[0].__int__(  )
        print pk
        return HttpResponse('/aluno/detail/%d' %(pk))

# Criando através de um txt com o seguinte modelo
# NúmeroQualquer Código Matrícula
# 99 ALLYUN MLGCIO KORFMREIA 136294648
def handle_criar_alunos_file(f, grupos):
    result = {"cadastrados": [], "erro": [] }
    count = 0

    for line in f:
        count += 1
        line = line.strip()
        if line.startswith("#") or not len(line):
            continue
        try:
            cod, nome_matricula = line.split(" ",1)
            nome, matricula = nome_matricula.rsplit(" ",1)
            first_name, last_name = nome.split(" ",1)
            username = matricula
            password = matricula

        except:
            result['erro'].append(('erro na linha '+str(count),'','','linha invalida'))
            continue
        
        query = Aluno.objects.filter(matricula = matricula)
        if len(query):
            result['erro'].append((username, matricula, "aluno com essa matricula já cadastrado"))
            for grupoId in grupos:
                grupo = Grupo.objects.get(pk=grupoId)
                grupo.alunos.add(Aluno.objects.get(pk=query[0].id))
                grupo.alunos
            grupo.save()
            continue
        
        query  = User.objects.filter(Q(username = username))
        if len(query):
            result['erro'].append((username, matricula, "aluno com esse usuário já cadastrado"))
            aluno = Aluno(matricula=matricula, user=query[0])
            for grupoId in grupos:
                grupo = Grupo.objects.get(pk=grupoId)
                grupo.alunos.add(aluno)
                grupo.alunos
            grupo.save()
            aluno.save()
            continue
        
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username)
        user.set_password(password)
        user.save()
        aluno = Aluno(matricula=matricula, user=user)

        for grupoId in grupos:
            grupo = Grupo.objects.filter(pk=grupoId)
            grupo.alunos.add(aluno)
            grupo.alunos
        grupo.save()
        
        aluno.save()
        result['cadastrados'].append(aluno)
    return result

@permission_required("core.professor", login_url="/home")
def criar_alunos(request):
    if request.method == 'POST':
        form = AlunosForm(request.POST, request.FILES)
        if form.is_valid():
            alunos = request.FILES['arquivo']      
            grupos = request.POST.getlist('grupos')
            result = handle_criar_alunos_file(alunos,grupos)
            return render_to_response('private/aluno/resultado.html', {'cadastrados' : result['cadastrados'], 'erro':result['erro']},
                              context_instance=RequestContext(request))
    else:
        form = AlunosForm()
    return render_to_response('private/aluno/alunos_form.html', {'form': form, 'professor':request.user.professor},
                              context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def aluno(request):
    objects_list = Aluno.objects.all()
    form = AlunoForm();
    multiform = AlunosForm();
    return render_to_response("private/aluno/list.html", {'object_list':objects_list, 'form':form, 'multiform': multiform},  context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def criar_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            with transaction.commit_on_success():
                grupo = Grupo(codigo = form.cleaned_data["codigo"], nome = form.cleaned_data["nome"], professor = request.user.professor,
                              about = form.cleaned_data["about"])
                grupo.save()
                return HttpResponseRedirect('/grupo')
    return HttpResponseRedirect('/grupo')

@permission_required("core.professor", login_url="/home")
def grupo(request):
    object_list = Grupo.objects.all();
    form = GrupoForm();
    return render_to_response("private/grupo/list.html", {'object_list': object_list, 'form': form},
                              context_instance=RequestContext(request));
                              
@permission_required("core.professor", login_url="/home")
def show_grupo(request, pk):
    grupo = Grupo.objects.get(pk=pk);
    form = GrupoAddAlunosForm(grupo);
    return render_to_response("private/grupo/grupo.html", {'grupo': grupo, 'form': form}, context_instance=RequestContext(request));
    
@permission_required("core.professor", login_url="/home")
def adicionar_alunos_grupo(request, pk):
    grupo = Grupo.objects.get(pk=pk)
    if request.method == 'POST':
        form = GrupoAddAlunosForm(grupo, request.POST)
        if form.is_valid():
            with transaction.commit_on_success():
                alunos = form.cleaned_data["alunos_disponiveis"]
                for aluno_id in alunos:
                    aluno = Aluno.objects.get(id = aluno_id)
                    grupo.alunos.add(aluno)
                grupo.save()
                return HttpResponseRedirect('/grupo')
            return HttpResponse('Deu Erro.')
    else:
        form = GrupoAddAlunosForm(grupo)
    
    return render_to_response('private/grupo/grupo.html', {'form':form, 'grupo':grupo}, context_instance=RequestContext(request))

    
