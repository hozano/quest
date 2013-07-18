# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.db.models.base import ModelBase
from django.http import HttpResponse, HttpResponseRedirect

from django.conf.urls.defaults import patterns

def create_crud_urls_from_model(model, urls="crud", form=None):
    app_label = model._meta.app_label
    verbose_name_url = model._meta.verbose_name.replace(" ", "")
    verbose_name = model._meta.verbose_name
    verbose_name_plural = model._meta.verbose_name_plural.capitalize()
    
    crud_urls = []
    
    if "c" in urls:
        params_dict = {'model':model,
                       'login_required':True,
                       'template_name':'generic_form.html', 
                       'post_save_redirect':'/%s/%s/page1' % (app_label, verbose_name_url), 
                       'extra_context':{'title':'Criar Novo %s' % verbose_name.capitalize() }}
        if form:
            params_dict.pop('model')
            params_dict['form_class'] = form
        crud_urls.append((r'^%s/%s/create/$' % (app_label, verbose_name_url), 
                         'django.views.generic.create_update.create_object', 
                         params_dict))
    if "r" in urls:
        crud_urls.append((r'^%s/%s/page(?P<page>[0-9]+)$' % (app_label, verbose_name_url), 
                        'ud.nucleo.views.generic_list', 
                        {'query_set':model.objects.all(),
                         'extra_context':{'title':'Lista dos %s' % (verbose_name_plural), 
                                          'link':'%s/%s' % (app_label, verbose_name_url) }}))
                                          
        crud_urls.append((r'^%s/%s/detail/(?P<object_id>\d+)$' % (app_label, verbose_name_url), 
                      'django.views.generic.create_update.update_object', 
                      {'model' : model,
                       'login_required':True, 
                       'template_name':'generic_detail.html', 
                       'extra_context':{'title':verbose_name.capitalize()}}))
    if "u" in urls:
        crud_urls.append((r'^%s/%s/update/(?P<object_id>\d+)$' % (app_label, verbose_name_url),
                      'django.views.generic.create_update.update_object', 
                      {'model': model,
                       'login_required':True, 
                       'template_name':'generic_form.html', 
                       'post_save_redirect':'/%s/%s/page1' % (app_label, verbose_name_url), 
                       'extra_context':{'title':'Editar %s' % verbose_name.capitalize()}}))
    if "d" in urls:
        crud_urls.append((r'^%s/%s/remove/(?P<object_id>\d+)$' % (app_label, verbose_name_url),
                      'django.views.generic.create_update.delete_object',
                      {'model': model,
                       'login_required':True,
                       'post_delete_redirect' : '/%s/%s/page1' % (app_label, verbose_name_url),
                       'extra_context' : {'title':'Exlcuir %s' % verbose_name.capitalize(),
                                          'link':'%s/%s' % (app_label, verbose_name_url) }}))
    
    if crud_urls:
        return patterns('', *crud_urls)
    
def create_crud_urls_from_models(model_list, urls="crud"):
    url_patterns = []
    for model in model_list:
        url_patterns += create_crud_urls_from_model(model, urls)
    return url_patterns
 
 
class JSONResponse(HttpResponse):
    def __init__(self,content='',json_opts={},mimetype="application/json",*args,**kwargs):
        if content:
            content = serialize_to_json(content,**json_opts)
        else:
            content = serialize_to_json([],**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

class LazyJSONEncoder(simplejson.JSONEncoder):
    def default(self,o):
        # this handles querysets and other iterable types
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        try:
            isinstance(o.__class__,ModelBase)
        except Exception:
            pass
        else:
            return force_unicode(o)

        return super(LazyJSONEncoder,self).default(obj)

def serialize_to_json(obj,*args,**kwargs):

    kwargs['ensure_ascii'] = kwargs.get('ensure_ascii',False)
    kwargs['cls'] = kwargs.get('cls',LazyJSONEncoder)


    return simplejson.dumps(obj,*args,**kwargs)

def qdct_as_kwargs(qdct):
    kwargs={}
    for k,v in qdct.items():
        kwargs[str(k)]=v
    return kwargs

def ajax_variavel(request):
    '''Filtra os valores existentes dde acordo com a variável 
    selecionada.
    '''
    if request.method == "POST":
        args = qdct_as_kwargs(request.POST)
        if args.has_key('id_variavel'):
            var=Variavel.objects.get(id=args['id_variavel'])
            valores = Valor.objects.filter(variavel=var)
            return JSONResponse(valores.values('id', 'valor'))
    return JSONResponse([{'id':'', 'valor':'---------'}])