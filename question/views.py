from django.shortcuts import render
from django.http import HttpResponse
from datareader.models import Topic,Question
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
def questions_vf(request):

    topic_list = list(Topic.objects.all())
    topic_list_context = []

    for topic in topic_list:
        topic_list_context.append({
            "name": topic.name,
            "questions": list(Question.filter_by_topic(topic.name)),
        })

    context = {
        'topic_list' : topic_list_context
    }

    return render(request, 'question/questions_vf.html', context)

@login_required()
def single_question_vf(request):

    if request.GET.get('topic'):
        topic = request.GET.get('topic', '')
    else:
        return (questions_vf(request))

    #Preguntas VF con tema "topic"
    question_list = list(Question.filter_by_topic(topic))
    question = question_list[0]


    context={
        'question': question,
        'topic' : topic,
    }
    return render(request,  'question/single_question_vf.html', context)