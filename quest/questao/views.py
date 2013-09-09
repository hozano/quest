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
    return render_to_response('private/questoes.html', context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def criar_questao(request, uid):
    if modulo_map.has_key(uid): #Resgata o modulo da questao a partir do UID
        modulo = modulo_map[uid]
        return modulo.criar_questao(request)
    else:
        return render_to_response('private/questao/index.html', 
                                  context_instance=RequestContext(request))

@permission_required("core.professor", login_url="/home")
def atualizar_questao(request, uid, pk):
    if modulo_map.has_key(uid): #Resgata o modulo da questao a partir do UID
        modulo = modulo_map[uid]
        return modulo.atualizar_questao(request, pk)
    else:
        return render_to_response('private/questao/index.html', 
                                  context_instance=RequestContext(request))


@permission_required("core.professor", login_url="/home")
def remover_questao(request,uid ,pk):
    if modulo_map.has_key(uid): #Resgata o modulo da questao a partir do UID
        modulo = modulo_map[uid]
        return modulo.remover_questao(request, pk)
    else:
        return render_to_response('private/questao/index.html',  context_instance=RequestContext(request))

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
    form = QuestionarioForm()
    if request.user.has_perm("core.professor"):
        questionarios = Questionario.objects.all().filter(criador=request.user)
    else:
        questionarios = []
        for i in request.user.aluno.grupo_set.all():
            questionarios += list(i.questionario_set.all())
    return render_to_response('private/questionarios.html', {'questionarios':questionarios, "form":form}, context_instance=RequestContext(request))


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
                return HttpResponseRedirect('/questionarios')
            return HttpResponse('Deu Erro.')
    return HttpResponseRedirect('/questionarios')

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
    return render_to_response('private/questionario/questionario.html', {'questionario':questionario}, context_instance = RequestContext(request))

def delete_questionario(request, pk):
    try:
        Questionario.objects.get(id = pk).delete()
        return HttpResponseRedirect('/questionarios')
    except:
        return HttpResponseRedirect('/questionarios')

@permission_required("core.professor", login_url="/home")
def aplicar_questionario(request, pk):
    questionario = Questionario.objects.get(pk = pk)
    grupos = Grupo.objects.filter(professor = request.user.professor)
    if request.method == 'POST':
        form = AplicarQuestionarioForm(grupos, request.POST)
        if form.is_valid():
            with transaction.commit_on_success():
                grupos = form.cleaned_data["grupos"]
                for grupo_id in grupos:
                    grupo = Grupo.objects.get(id = grupo_id)
                    questionario.grupos.add(grupo)
                questionario.save()
                return HttpResponseRedirect('/questionarios')
    else:
        form = AplicarQuestionarioForm(grupos)
    return render_to_response('private/questionario/aplicar_questionario.html', {'form':form, 'questionario':questionario},  context_instance=RequestContext(request))
 
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
        forms = SubmissaoFormSet(request.POST)
        forms.forms = make_forms_from_questionario(questionario, request.POST)
        if forms.is_valid():
            old = Submissao.objects.filter(questionario = questionario, aluno = request.user.aluno)
            if old:
                old.delete()
            submissao = Submissao(questionario = questionario, aluno = request.user.aluno)
            submissao.save()
            for form in forms:
                resposta = form.save(commit=False)
                resposta.questao = form.questao
                resposta.submissao = submissao
                resposta.save()
            return render_to_response('private/mensagem_generica.html', {'msg':"Sua submissão foi salva com sucesso", 'link':'/submissoes'}, context_instance = RequestContext(request))
    else:
        forms = SubmissaoFormSet()
        forms.forms = make_forms_from_questionario(questionario)
    return render_to_response('private/submissao/submissao_form.html', {'questionario':questionario, "forms":forms}, context_instance = RequestContext(request))


@permission_required("core.professor", login_url="/home")
def pontuar_submissao(request, pk):
    submissao = Submissao.objects.get(id=pk)
    if request.method == 'POST':
        nota = request.POST.get('pts')
        print nota
        submissao.nota = nota
        submissao.save()
        return HttpResponseRedirect('/submissoes')
    return render_to_response('private/submissao/submissao.html',{"submissao":submissao}, context_instance=RequestContext(request))
        
@login_required
def submissao(request):
    if(request.user.has_perm("core.professor")):
        submissoes = Submissao.objects.all();
    else:
        submissoes = Submissao.objects.filter(aluno = request.user.aluno)
    return render_to_response('private/submissao/submissoes.html', {'submissoes':submissoes}, context_instance=RequestContext(request))