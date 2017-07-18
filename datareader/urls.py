from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'concept', views.concept, name='concept'),
    url(r'populate_test', views.populate_test, name='populate_test'),
    url(r'auto_evaluacion', views.auto_evaluacion, name='autoevaluacion'),
]

