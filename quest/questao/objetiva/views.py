# coding:utf-8
from django.shortcuts import render_to_response, RequestContext
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from forms import QuestaoObjetivaForm, AlternativaObjetivaFormSet
from models import AlternativaQuestao, QuestaoObjetiva
from django.contrib.auth.decorators import login_required, permission_required

@permission_required("core.professor", login_url="/home")
def criar_questao(request):
    if request.method == 'POST':
        form = QuestaoObjetivaForm(request.POST)
        formset = AlternativaObjetivaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            questao = form.save(commit=False)
            questao.criador = request.user
            questao.save()
            questao.tags = form.cleaned_data['tags']
            for form_dict in formset.cleaned_data:
                if form_dict:
                    alternativa = AlternativaQuestao()
                    alternativa.questao = questao
                    alternativa.alternativa = form_dict['alternativa']
                    alternativa.valor = form_dict['valor']
                    alternativa.save()
            return HttpResponseRedirect('/questoes')
    else:
        form = QuestaoObjetivaForm()
        formset = AlternativaObjetivaFormSet()
        
    return render_to_response('private/questao/objetiva/form.html', {'form':form, 'formset':formset}, 
                                      context_instance=RequestContext(request))


   
@permission_required("core.professor", login_url="/home")
def atualizar_questao(request, pk):
    questao = QuestaoObjetiva.objects.get(id = pk)
    if (request.method == 'POST'):
        form = QuestaoObjetivaForm(request.POST)
        formset = AlternativaObjetivaFormSet(request.POST)
        if form.is_valid() and formset.is_valid(): 
            query = QuestaoObjetiva.objects.get(id = pk)
            query.nome = form.cleaned_data['nome']
            query.enunciado = form.cleaned_data['enunciado']
            query.nivel_estatico = form.cleaned_data['nivel_estatico']
            query.tags = form.cleaned_data['tags']
            query.save()
            AlternativaQuestao.objects.filter(questao = query).delete()
            for form_dict in formset.cleaned_data:
                if form_dict:
                    alternativa = AlternativaQuestao()
                    alternativa.questao = query
                    alternativa.alternativa = form_dict['alternativa']
                    alternativa.valor = form_dict['valor']
                    alternativa.save()
            return HttpResponseRedirect('/questao/detail/%s/%s' % (questao.uid(), questao.id))
    else:
        form = QuestaoObjetivaForm(initial={'nome':questao.nome, 'enunciado':questao.enunciado, 
                                        'criador':questao.criador, 'data_criacao':questao.data_criacao, 
                                        'nivel_estatico':questao.nivel_estatico, 'nivel_dinamico':questao.nivel_dinamico, 
                                        'questionarios':questao.questionarios, 'tags':questao.get_tags_as_string})

        queryset= AlternativaQuestao.objects.filter(questao = questao).values()
        formset = AlternativaObjetivaFormSet(initial=queryset)
    return render_to_response('private/questao/objetiva/show.html', {'questao':questao, 'form':form, 'formset':formset}, context_instance=RequestContext(request))

@login_required
def show_questao(request, pk):
    questao = QuestaoObjetiva.objects.get(id = pk)
    form = QuestaoObjetivaForm(initial={'nome':questao.nome, 'enunciado':questao.enunciado, 
                                        'criador':questao.criador, 'data_criacao':questao.data_criacao, 
                                        'nivel_estatico':questao.nivel_estatico, 'nivel_dinamico':questao.nivel_dinamico, 
                                        'questionarios':questao.questionarios, 'tags':questao.get_tags_as_string})
    queryset= AlternativaQuestao.objects.filter(questao = questao).values()
    formset = AlternativaObjetivaFormSet(initial=queryset)
    return render_to_response('private/questao/objetiva/show.html', {'questao':questao, 'form':form, 'formset':formset}, 
                              context_instance=RequestContext(request))
    
@permission_required("core.professor", login_url="/home")
def remover_questao(request, pk):
    try:
        QuestaoObjetiva.objects.get(id = pk).delete()
        return render_to_response ('private/mensagem_generica.html',{'link':'/questoes', 'msg':'Questão apagada com sucesso!'}, context_instance=RequestContext(request))
    except:
        return render_to_response('private/mensagem_generica.html', {"msg":"Não foi possível remover a questao", 'link':'/questoes'},
                                  context_instance=RequestContext(request))