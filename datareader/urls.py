from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'concept$', views.concept, name='concept'),
    url(r'populate_test', views.populate_test, name='populate_test'),
    url(r'auto_evaluacion', views.auto_evaluacion, name='autoevaluacion'),

    url(r'admin_site', views.admin_site, name='admin_site'),
    url(r'update_concepts$', views.update_concepts, name='update_concepts'),
    url(r'update_questions_vf$', views.update_questions_vf, name='update_questions_vf'),
    url(r'update_questions_opm$', views.update_questions_opm, name='update_questions_opm', ),
]

