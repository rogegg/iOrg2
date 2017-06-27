from django.conf.urls import url

from django.contrib.auth.views import login
import datareader.views
from django.contrib.auth import views as authViews
from . import views


urlpatterns = [
    url(r'^$',        views.index, name='index'),
    url(r'^signup$',  views.signup, name='signup'),
    url(r'^login$',   authViews.login, {'template_name': 'user/login.html',}, name='login'),
    url(r'^logout$',  authViews.logout, {'next_page': 'login'}, name="logout"),
    # url(r'^logout$',  views.logout, name='logout'),
    # url(r'^concept$', datareader.views.concept, name='concept'),
]

