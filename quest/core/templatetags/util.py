from django import template
from quest.core.models import Questao, QuestaoObjetiva, QuestaoSubjetiva, QuestaoVF

register = template.Library()

@register.simple_tag
def get_alternativas_form(questao_id):
    questao = Questao.objects.get(id=questao_id)
    questao = questao.concrete()
    
    html = ''
    if isinstance(questao, QuestaoObjetiva):
        for alternativa in questao.alternativaquestao_set.all():
            html += "<input type='radio' name='%s' value='%s'/> %s <br/>" % (alternativa.questao_id, alternativa.id, alternativa.alternativa)
    elif isinstance(questao, QuestaoVF):
        for alternativa in questao.alternativaquestao_set.all():
            html += "V <input type='radio' name='%s' value='%s'/><input type='radio' name='%s' value='0'/> F - %s <br/>" % (alternativa.id, alternativa.id, alternativa.id, alternativa.alternativa)
    elif isinstance(questao, QuestaoSubjetiva):
        html = "<textarea name='%s' rows=8 cols=90></textarea><br/>" % (questao.id)
    return html