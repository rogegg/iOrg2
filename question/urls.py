from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.questions_vf, name='vf'),
    url(r'vf$', views.questions_vf, name='vf'),
    url(r'vf/single/$', views.single_question_vf, name='vf_single'),
]

