from django.shortcuts import render
from django.contrib.auth.models import Permission,User, Group

from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import models, migrations
from django.shortcuts import redirect


import gspread
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from datareader import models
import datareader

LOCK = False #Variable cerrojo

# Create your views here.
def index(request):
    return render(request,'index.html')


@login_required()
def concept(request):

    topic_list = []

    #creamos los datos necesarios para la plantilla html
    for i in range(0,len(Topic.objects.all())):
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

    populate = populate_concept_page()

    # populate = Concept.objects.get(name="Primer concepto")
    all_concepts = Concept.objects.all()
    context = {'object_list': all_concepts}
    # context = {'object_list': populate}

    #return HttpResponse("<p>HEEEEEEEEEEEE</p>")
    return render(request, 'datareader/populate_test.html', context)

@login_required()
def auto_evaluacion(request):
    return render(request, 'autoevaluacion.html')


@login_required()
def admin_site(request):
    return render(request, 'user/admin_site.html')


@login_required()
def update_concepts(request):
    global LOCK
    if not LOCK:
        LOCK = True
        populate_concept_page()
        LOCK = False
    return render(request, 'user/admin_site.html',{"status_concepts":True})


@login_required()
def update_questions_vf(request):
    global LOCK
    if not LOCK:
        LOCK = True
        populate_questions("vf")
        LOCK = False
    return render(request, 'user/admin_site.html',{"status_questions_vf":True})


@login_required()
def update_questions_opm(request):
    user = request.user
    permission_len = len(Permission.objects.filter(user=user).filter(codename="add_concept"))
    if permission_len>0:
        global LOCK
        if not LOCK:
            LOCK = True
            populate_questions_opm()
            LOCK = False
        return render(request, 'user/admin_site.html',{"status_questions_opm":True})
    else:
        return redirect('index')

