from quest.questao.models import modulos

def modulos_processor(request):
    return {'modulos':modulos,}
