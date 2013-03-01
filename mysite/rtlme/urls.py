from django.conf.urls import patterns, url
from django.views.generic import DetailView
from models import Result

import views

urlpatterns = patterns('',
   # ex: /rtlme/
   url(r'^$', views.index, name='index'),
   # ex: /rtlme/5/
   url(r'^(?P<pk>\d+)/$',
       DetailView.as_view(model=Result, template_name='rtlme/result.html'),
       name="result"),
   # ex: /rtlme/rtl/
   url(r'^rtl/$', views.rtl, name='rtl')
)