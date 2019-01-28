# coding: utf-8

from django.conf.urls import patterns, url
from soc_scan import views

urlpatterns = patterns(
    '',
    # 搜索
    url(r'^search/dts$', views.SecrchView.as_view()),
    # 任务
    url(r'^task$', views.TaskView.as_view()),
    # 任务列表
    url(r'^task/dts$', views.TaskList.as_view()),
    # 任务复测
    url(r'^task/check$', views.TaskCheck.as_view()),
    # 任务详情
    url(r'^task/(?P<id>\w+)$', views.TaskView.as_view()),

    # 任务扫描结果
    url(r'^task/result/dts$', views.TaskResultList.as_view()),
    # 插件
    url(r'^plugin$', views.PluginView.as_view()),
    # 插件列表
    url(r'^plugin/dts$', views.PluginList.as_view()),
    # 插件列表
    url(r'^plugin/type$', views.PluginTypeList.as_view()),
    # 插件更新
    url(r'^plugin/pull$', views.PluginPull.as_view()),
    # 配置
    url(r'^config/info$', views.ConfigInfoView.as_view()),
    # 修改配置
    url(r'^config/update$', views.ConfigUpdateView.as_view()),
)
