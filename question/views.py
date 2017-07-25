from django.shortcuts import render
from django.shortcuts import redirect
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
        'topic_list' : topic_list_context,
        "type": "vf",
    }
    return render(request, 'question/questions.html', context)

@login_required()
def questions_opm(request):

    topic_list = list(Topic.objects.all())
    topic_list_context = []

    for topic in topic_list:
        topic_list_context.append({
            "name": topic.name,
            "questions": list(Question.filter_by_topic(topic.name)),

        })

    context = {
        'topic_list' : topic_list_context,
        "type": "opm",
    }
    return render(request, 'question/questions.html', context)


@login_required()
def single_question(request):
    if request.GET.get('topic'):
        topic = request.GET.get('topic', '')
        type  = request.GET.get('type', '')
    else:
        return (questions_vf(request))

    #Preguntas VF con tema "topic"
    question_list = list(Question.filter_by_topic(topic).filter(type=type))
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
            "type": type,
        }
        return render(request, 'question/question_response.html', context_response)

    context={
        'question': question,
        'topic' : topic,
        'question_options' : new_list,
        'form' : AnswerForm(),
    }
    return render(request,  'question/single_question.html', context)


def question_response(request):

    if request.method == 'POST':
        return render(request, 'question/test_form.html', {"message":request.POST.get("options")} )

    return render(request, 'question/test_form.html',{"message":"NO POST"})


@login_required()
def exam_type(request):
    return render(request, 'question/exam_type.html')


def generate_exam_vf():
    question_list = Question.objects.filter(type='vf')
    topic_list = Topic.objects.all()
    topic_obj = {}
    exam = []
    for topic in topic_list:
        questions_topic = question_list.filter(topic = topic)
        if(len(list(questions_topic)) > 0 and topic.name!="Introducción"):
            #quedarse con 2 preguntas de cada tema
            topic_obj[topic.name] = questions_topic.order_by('?')[:2]
            exam.append({
                "topic": topic.name,
                "questions": list(questions_topic.order_by('?')[:2]),
            })

    return exam

@login_required()
def exam_vf(request):
    exam = {}
    # Si El formulario está relleno lo procesamos
    if request.method == 'POST':
        print("POST")
        response_list = []
        questions_id_list = []
        options_list = []
        count_ok = 0            #Número de respuestas correctas
        count_error = 0         #Número de respuestas incorrectas
        count_no_response = 0   #nÚmero de respuestas sin responder
        score = 0               #puntuación total del examen
        score_ok = 0.5          #puntuación para respuesta correcta
        score_error = -0.25     #puntuacion para respuesta incorrecta
        for i in range(1,20):
            if(request.POST.get("question-" + str(i) + "-1") == None):
                break
            question_id_1 = request.POST.get("question-" + str(i) + "-1")
            option_selected_1 = (request.POST.get("option-" + str(question_id_1)))
            question_id_2 = request.POST.get("question-" + str(i) + "-2")
            option_selected_2 = (request.POST.get("option-" + str(question_id_2)))
            #comprobamos si es respuesta que resta, suma o no influye
            if(option_selected_1 == None):
                count_no_response=count_no_response+1
            elif(Question.objects.get(id=question_id_1).answer == option_selected_1):
                count_ok = count_ok+1
                score = score + score_ok
            else:
                count_error = count_error+1
                score = score + score_error

            if (option_selected_2 == None):
                count_no_response = count_no_response + 1
            elif (Question.objects.get(id=question_id_2).answer == option_selected_2):
                count_ok = count_ok + 1
                score = score + score_ok
            else:
                count_error = count_error + 1
                score = score + score_error

            response_list.append({
                "question": Question.objects.get(id=question_id_1),
                "option_selected": option_selected_1,
            })
            response_list.append({
                "question": Question.objects.get(id=question_id_2),
                "option_selected": option_selected_2,
            })

        # Ponderamos nota sobre 10
        n_questions = len(response_list)
        score_t = (score * 10.0) / (n_questions * score_ok)

        print("Número de preguntas -> ", n_questions)
        print("Score bruto         -> ", score)
        print("Score sobre 10      -> ", score_t)
        print("n_questions * score_ok      -> ", n_questions*score_ok)

        total_score={
            "count_ok": count_ok,
            "count_error": count_error,
            "count_no_response":count_no_response,
            "score": score,
        }

        return render(request, 'question/exam_vf.html', {"response_list":response_list,"total_score":total_score})
    # si el formulario no está relleno , lo generamos
    else:
        exam = generate_exam_vf()
        return render(request, 'question/exam_vf.html', {"exam":exam})





