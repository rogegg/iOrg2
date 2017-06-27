from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import models, migrations

import gspread
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from datareader import models
import datareader

# Create your views here.
def index(request):
    return render(request,'index.html')


@login_required()
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