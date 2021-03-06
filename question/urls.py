from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.questions_vf, name='vf'),
    url(r'vf$', views.questions_vf, name='vf'),
    url(r'opm$', views.questions_opm, name='opm'),
    url(r'vf/single/$', views.single_question, name='vf_single'),
    url(r'opm/single/$', views.single_question, name='opm_single'),
    url(r'vf/question_response$', views.question_response, name='question_response'),
    url(r'exam_type', views.exam_type, name='exam_type'),
    url(r'vf/exam', views.exam_vf, name='exam_vf'),
    url(r'opm/exam', views.exam_opm, name='exam_opm'),
]

