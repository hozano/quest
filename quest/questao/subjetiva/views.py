# coding:utf-8
from django.shortcuts import render_to_response, RequestContext
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from forms import QuestaoSubjetivaForm
from django.contrib.auth.decorators import login_required, permission_required
from models import QuestaoSubjetiva

@permission_required("core.professor", login_url="/home")
def criar_questao(request):
    if request.method == 'POST':
        form = QuestaoSubjetivaForm(request.POST)
        if form.is_valid():
            questao = form.save(commit=False)
            questao.criador = request.user
            questao.save()
            questao.tags = form.cleaned_data['tags']
            return HttpResponseRedirect('/questoes')
    else:
        form = QuestaoSubjetivaForm()
    return render_to_response('private/questao/subjetiva/form.html', {'form':form}, 
                                      context_instance=RequestContext(request))
@login_required
def show_questao(request, pk):
    questao = QuestaoSubjetiva.objects.get(id = pk)
    form = QuestaoSubjetivaForm(initial={'nome':questao.nome, 'enunciado':questao.enunciado,'resposta':questao.resposta ,
                                        'criador':questao.criador, 'data_criacao':questao.data_criacao, 
                                        'nivel_estatico':questao.nivel_estatico, 'nivel_dinamico':questao.nivel_dinamico, 
                                        'questionarios':questao.questionarios, 'tags':questao.get_tags_as_string})
    return render_to_response('private/questao/subjetiva/show.html', {'questao':questao, 'form':form}, 
                              context_instance=RequestContext(request))   

@permission_required("core.professor", login_url="/home")
def atualizar_questao(request, pk):
    questao = QuestaoSubjetiva.objects.get(id = pk)
    if (request.method == 'POST'):
        form = QuestaoSubjetivaForm(request.POST)
        if form.is_valid():
            query = QuestaoSubjetiva.objects.get(id = pk)
            query.nome = form.cleaned_data['nome']
            query.enunciado = form.cleaned_data['enunciado']
            query.resposta = form.cleaned_data['resposta']
            query.criador = questao.criador
            query.data_criacao = questao.data_criacao
            query.nivel_estatico = form.cleaned_data['nivel_estatico']
            query.nivel_dinamico = questao.nivel_dinamico
            query.questionarios = questao.questionarios.all()
            query.tags = form.cleaned_data['tags']
            query.save()
            return render_to_response ('private/mensagem_generica.html',{'link':'/questoes', 'msg':'Questão alterada com sucesso!'},
                                       context_instance = RequestContext(request))
    else:
        form = QuestaoSubjetivaForm(initial={'nome':questao.nome, 'enunciado':questao.enunciado,'resposta':questao.resposta ,
                                        'criador':questao.criador, 'data_criacao':questao.data_criacao, 
                                        'nivel_estatico':questao.nivel_estatico, 'nivel_dinamico':questao.nivel_dinamico, 
                                        'questionarios':questao.questionarios, 'tags':questao.get_tags_as_string})

    return render_to_response('private/questao/subjetiva/form.html', {'questao':questao, 'form':form}, 
                              context_instance=RequestContext(request))

    
@permission_required("core.professor", login_url="/home")
def remover_questao(request, pk):
    try:
        QuestaoSubjetiva.objects.get(id = pk).delete()
        return render_to_response ('private/mensagem_generica.html',{'link':'/questoes', 'msg':'Questão apagada com sucesso!'},
                                   context_instance=RequestContext(request))
    except:
        return render_to_response('private/mensagem_generica.html', {"msg":"Não foi possível remover a questao", 'link':'/questoes'},
                                  context_instance=RequestContext(request))