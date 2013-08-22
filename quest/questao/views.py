#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from quest.questao.models import modulo_map, Questionario, get_questoes,  Submissao
from quest.questao.forms import QuestionarioForm, AplicarQuestionarioForm,\
    SubmissaoForm, make_forms_from_questionario
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from quest.core.models import Grupo, Aluno
from django.forms.formsets import formset_factory, BaseFormSet

from datetime import datetime


@permission_required("core.professor", login_url="/home")
def questoes(request):
    '''Redireciona para a página principal.
    
    @param request: Requisição
    @type request: HttpRequest
    @return: Página principal
    @rtype: HttpResponse
    ''' 
    return render_to_response('private/questoes.html', {'questoes':get_questoes()}, 
                              context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def criar_questao(request, uid):
    if modulo_map.has_key(uid): #Resgata o modulo da questao a partir do UID
        modulo = modulo_map[uid]
        return modulo.criar_questao(request)
    else:
        print "Não foi possível criar a questao"
        return render_to_response('private/questao/index.html', 
                                  context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def atualizar_questao(request, uid, pk):
    if modulo_map.has_key(uid): #Resgata o modulo da questao a partir do UID
        modulo = modulo_map[uid]
        return modulo.atualizar_questao(request, pk)
    else:
        print "Não foi possível atualizar a questao"
        return render_to_response('private/questao/index.html', 
                                  context_instance=RequestContext(request))


@permission_required("core.professor", login_url="/home")
def remover_questao(request,uid ,pk):
    if modulo_map.has_key(uid): #Resgata o modulo da questao a partir do UID
        modulo = modulo_map[uid]
        print modulo
        return modulo.remover_questao(request, pk)
    else:
        print "Não foi possível remover a questao"
        return render_to_response('private/questao/index.html', 
                                  context_instance=RequestContext(request))

@login_required
def show_questao(request, uid, pk):
    if modulo_map.has_key(uid): #Resgata o modulo da questao a partir do UID
        modulo = modulo_map[uid]
        return modulo.show_questao(request, pk)
    else:
        print "Não foi possível exibir a questao"
        return render_to_response('private/questao/index.html', 
                                  context_instance=RequestContext(request))

@login_required
def questionarios(request):
    '''Redireciona para a página principal.
    
    @param request: Requisição
    @type request: HttpRequest
    @return: Página principal
    @rtype: HttpResponse
    '''
    
    if request.user.has_perm("core.professor"):
        questionarios = Questionario.objects.all().filter(criador=request.user)
    else:
        questionarios = []
        for i in request.user.aluno.disciplina_set.all():
            questionarios += list(i.questionario_set.all())
    return render_to_response('private/questionario/index.html', {'questionarios':questionarios}, context_instance=RequestContext(request))


@permission_required("core.professor", login_url="/home")
def criar_questionario(request):
    if request.method == 'POST':
        form = QuestionarioForm(request.POST)
        if form.is_valid():
            with transaction.commit_on_success():
                questionario = form.save(commit=False)
                questionario.criador = request.user
                questionario.save()
                questoes = form.cleaned_data['questoes']
                for id_questao in questoes:
                    uid,_id = id_questao.split('#')
                    questao = modulo_map[uid].classe.objects.get(id=_id)
                    questao.questionarios.add(questionario)
                    questao.save()    
                return HttpResponseRedirect('/questionario/pontuar/%i' % (questionario.id))
                
            return HttpResponse('Deu Erro.')
    else:
        form = QuestionarioForm()
        
    return render_to_response('private/questionario/form.html', {'form':form}, 
                                      context_instance=RequestContext(request))

def pontuar_questionario(request, pk):
    questionario = Questionario.objects.get(id=pk)
    questao = questionario.get_questoes()
    if request.method == 'POST':
        form_list = request.POST.getlist('pts')
        dic = questionario.pontuar(form_list)
        questionario.dicionario = dic
        questionario.save()
        return HttpResponseRedirect('/questionarios')
    else:
        return render_to_response('private/questionario/pontuar.html',{'questao':questao,'questionario':questionario}, 
                                      context_instance=RequestContext(request))
    
@login_required
def show_questionario(request, pk):
    questionario = Questionario.objects.get(id = pk)
    link = "/questionario/detail/%s" % pk
        
    return render_to_response('private/questionario/questionario.html', {'questionario':questionario, "link":link},
                              context_instance = RequestContext(request))

@permission_required("core.professor", login_url="/home")
def aplicar_questionario(request, pk):
    questionario = Questionario.objects.get(pk = pk)
    disciplinas = Grupo.objects.filter(professor = request.user.professor)
    if request.method == 'POST':
        form = AplicarQuestionarioForm(disciplinas, request.POST)
        if form.is_valid():
            with transaction.commit_on_success():
                disciplinas = form.cleaned_data["disciplinas"]
                for disciplina_id in disciplinas:
                    disciplina = Grupo.objects.get(id = disciplina_id)
                    questionario.disciplinas.add(disciplina)
                print "disciplinas no questionario ", questionario.disciplinas.all()
                questionario.save()
              
                return HttpResponseRedirect('/questionarios')
            
    form = AplicarQuestionarioForm(disciplinas)
    return render_to_response('private/questionario/aplicar_questionario.html', {'form':form, 'questionario':questionario}, 
                              context_instance=RequestContext(request))
 
@login_required
def submeter_questionario(request, pk):
    questionario = Questionario.objects.get(pk = pk)
    if datetime.now() > questionario.hora_fim:
        return HttpResponseRedirect('/questionario/detail/'+pk)
    SubmissaoFormSet = formset_factory(SubmissaoForm, formset=BaseFormSet)
    if request.method == 'POST':
        request.POST['form-TOTAL_FORMS'] = u'%s'%len(questionario.get_questoes())
        request.POST['form-INITIAL_FORMS']= u'0'
        request.POST['form-MAX_NUM_FORMS'] = u''
        questoes = SubmissaoFormSet(request.POST)
        questoes.forms = make_forms_from_questionario(questionario, request.POST)
        if questoes.is_valid():
            submissao = Submissao(questionario = questionario, aluno = request.user.aluno)
            submissao.save()
            for form in questoes:
                resposta = form.save(commit=False)
                resposta.questao = form.questao
                resposta.submissao = submissao
                resposta.save()
            return render_to_response('private/mensagem_generica.html', {'msg':"Sua submissão foi salva com sucesso", 'link':'/submissoes'})
    else:
        questoes = SubmissaoFormSet()
        questoes.forms = make_forms_from_questionario(questionario)
    return render_to_response('private/submissao/submissao_form.html', {'questionario':questionario, "questoes":questoes},
                              context_instance = RequestContext(request))


@permission_required("core.professor", login_url="/home")
def pontuar_submissao(request, pk):
    submissao = Submissao.objects.get(id=pk)
    if request.method == 'POST':
        nota = request.POST.get('pts')
        submissao.nota = nota
        submissao.save()
        return HttpResponseRedirect('/submissoes')
    else:
        return render_to_response('private/submissao/pontuar.html',{}, context_instance=RequestContext(request))
        

@login_required
def listar_submissoes(request, disciplina_id=None, aluno_id=None, questionario_id=None):
    hasperm = request.user.has_perm("core.professor")
    
    if not disciplina_id:
        if hasperm:
            disciplinas = Grupo.objects.filter(professor = request.user.professor)
        else:
            disciplinas = Grupo.objects.filter(alunos = request.user.aluno)
        return render_to_response("private/submissao/list.html", {"disciplinas":disciplinas}, 
                                  context_instance = RequestContext(request))
    else:
        disciplina = Grupo.objects.get(pk = disciplina_id)
        if aluno_id:
            if questionario_id:
                aluno = Aluno.objects.get(id = aluno_id)
                submissoes = Questionario.objects.get(id = questionario_id).submissao_set.filter(aluno = aluno)
                return render_to_response("private/submissao/list.html", {"submissoes": submissoes, "disciplina":disciplina_id,
                       "link":"/%s/aluno_%s" % (disciplina_id, aluno_id)}, context_instance = RequestContext(request))
            else:
                questionarios = Questionario.objects.filter(disciplinas = disciplina)
                return render_to_response("private/submissao/list.html", {"questionarios":questionarios, "disciplina":disciplina_id,
                       "aluno":aluno_id, "link":"/disciplina_%s" % disciplina_id},  context_instance = RequestContext(request))
        elif questionario_id:
            questionario = Questionario.objects.get(id = questionario_id)
            submissoes = questionario.submissao_set.filter(aluno = request.user.aluno)
            return render_to_response("private/submissao/list.html", {"submissoes": submissoes, "disciplina":disciplina_id, 
                                        "link":"/disciplina_%s" % disciplina_id}, context_instance = RequestContext(request))
        else:
            if hasperm:
                alunos = disciplina.alunos.all()
                return render_to_response("private/submissao/list.html", {"disciplina":disciplina_id, "alunos":alunos}, 
                                      context_instance = RequestContext(request))
            else:
                questionarios = Questionario.objects.filter(disciplinas = disciplina)
                return render_to_response("private/submissao/list.html", {"questionarios":questionarios, "disciplina":disciplina_id},  
                                          context_instance = RequestContext(request))
