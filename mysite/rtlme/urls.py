from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
   # ex: /rtlme/
   url(r'^$', views.index, name='index'),
   # ex: /rtlme/5/
   url(r'^(?P<result_id>\d+)/$', views.result, name='result'),
   # ex: /rtlme/rtl/
   url(r'^rtl/$', views.rtl, name='rtl')
)