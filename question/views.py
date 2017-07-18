from django.shortcuts import render
from django.http import HttpResponseRedirect
from datareader.models import Topic,Question
from .models import AnswerForm
from django.contrib.auth.decorators import login_required
from django.db import models, migrations

import random


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
    question = random.choice(question_list)
    question_options = question.get_option_list()
    i=0
    new_list = []
    for option in question_options:
        new_list.append({"name":option,"id":i})
        i=i+1

    #si se ha enviado el formulario, mostramos la respuesta,
    #si no, mostramos una pregunta nueva.
    if request.method == 'POST':
        option_select = request.POST.get("options")
        question = Question.objects.get(name=request.POST.get("question"))
        response = False # Respuesta falsa
        if option_select == question.answer:
            response = True #Respuesta correcta

        context_response = {
            "question": question,
            "response": response,
        }
        return render(request, 'question/question_response.html', context_response)

    context={
        'question': question,
        'topic' : topic,
        'question_options' : new_list,
        'form' : AnswerForm(),
    }
    return render(request,  'question/single_question_vf.html', context)


def question_response(request):

    if request.method == 'POST':
        return render(request, 'question/test_form.html', {"message":request.POST.get("options")} )

    return render(request, 'question/test_form.html',{"message":"NO POST"})

