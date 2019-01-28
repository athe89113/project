# coding: utf-8

from django.conf.urls import patterns, url
from soc_datatable import datatable_views
from soc_datatable import views

urlpatterns = patterns(
    '',
    # 日志审计
    url(r'^system/soclog/dts$', views.Soclog.as_view()),

)
