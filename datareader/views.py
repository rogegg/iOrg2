from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db import models, migrations

import gspread
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from datareader import models
import datareader

# Create your views here.
def index(request):
    #gc = gspread.login('iorgugr@gamil.com', 'i20Org17?')


    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('iOrgTest-5fa50b4936cd.json', scope)
    # gc = gspread.authorize(httplib2.Http(credentials))

    gc = gspread.authorize(credentials)
    sh = gc.open("iOrg2.0")
    wks = sh.get_worksheet(2)
    value = wks.acell('A2').value # valor de la celda A2
    title = wks.cell(1,7).value
    value = wks.cell(2, 7).value # valor de la celda con posición fila 2 y columna 1
    # wks.update_acell('B2', 'Im your server') # Necesitamos dar permisos de edición a estos credenciales.


    code = "<html><body> <h2>"+title+"</h2><br><p>" +value+ "</p> </body></html>"
    return HttpResponse(code)


def concept(request):

    topic_list = []

    #creamos los datos necesarios para la plantilla html
    for i in range(0,len(Topic.objects.all())) :
        topic_list.append({
            "name" : Topic.objects.all()[i].name,
            "subtopics" : []
        })
        for j in range(0,len( SubTopic.objects.filter(topic=Topic.objects.all()[i]) )):
            topic_list[i]["subtopics"].append({
                "name" : SubTopic.objects.filter(topic=Topic.objects.all()[i])[j].name,
                "concepts" : Concept.objects.filter(subtopic=SubTopic.objects.filter(topic=Topic.objects.all()[i])[j])
            })





    context = {
        'topic_list' : topic_list
    }

    #return HttpResponse("<p>HEEEEEEEEEEEE</p>")
    return render(request, 'datareader/concepts.html', context)

def populate_test(request):
    concept_list = Concept.objects.all()
    # a = Concept.objects.get(name="Primer concepto")
    # c = Concept.objects.get(name="Primer concepto")

    # concept_list = [a,c]
    # context = {'object_list': a}
    # context = {'object_list': concept_list}

    populate = populate_models()

    # populate = Concept.objects.get(name="Primer concepto")
    all_concepts = Concept.objects.all()
    context = {'object_list': all_concepts}
    # context = {'object_list': populate}

    #return HttpResponse("<p>HEEEEEEEEEEEE</p>")
    return render(request, 'datareader/populate_test.html', context)