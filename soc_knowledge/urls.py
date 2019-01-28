# coding=utf-8
from django.conf.urls import patterns, url
from soc_knowledge import views

urlpatterns = patterns(
    '',
    # 漏洞库
    url(r'^vul/dts$', views.VulLibraryList.as_view()),
    url(r'^vul/detail/(?P<pk>\d+)$', views.VulDetail.as_view()),
    url(r'^vul/quick_search$', views.QuickSearchVul.as_view()),
    url(r'^vul/similar/(?P<tp>\w+)$', views.SimilarVul.as_view()),
    url(r'^vul/last_search', views.LastVulSearch.as_view()),
    url(r'^vul/last_high_vul', views.LastHighVul.as_view()),
    url(r'^vul/data_source', views.VulDataSource.as_view()),
    url(r'^vul/vul_score/(?P<pk>\d+)$', views.VulScore.as_view()),
    # url(r'^vul/vul_score$', views.VulScoreCalculation.as_view()),
    url(r'^vul/version$', views.VulVersion.as_view()),
    # 知识库
    url(r'^knowledge/dts$', views.KnowledgeList.as_view()),
    url(r'^knowledge/add$', views.KnowledgeAdd.as_view()),
    url(r'^knowledge/detail/(?P<pk>\d+)$', views.KnowledgeDetail.as_view()),
    url(r'^knowledge/last_add$', views.LastAddKnowledge.as_view()),
    url(r'^knowledge/similar$', views.SimilarKnowledge.as_view()),
    url(r'^knowledge/attr$', views.KnowledgeAttrList.as_view()),
    url(r'^knowledge/last_search$', views.LastKnowledgeSearch.as_view()),
    # 预案库
    url(r'^plan/dts$', views.PlanList.as_view()),
    url(r'^plan/last_add$', views.LastAddPlan.as_view()),
    url(r'^plan/last_search$', views.LastPlanSearch.as_view()),
    url(r'^plan/add$', views.PlanAdd.as_view()),
    url(r'^plan/detail/(?P<pk>\d+)$', views.PlanDetail.as_view()),
    url(r'^plan/attr$', views.PlanAttrList.as_view()),
    url(r'^plan/similar/(?P<tp>\w+)$', views.PlanSimilar.as_view()),
    url(r'^plan/hot$', views.PlanHot.as_view()),
    url(r'^plan/contacts/dts$', views.PlanContactsList.as_view()),
    url(r'^plan/contacts/(?P<pk>\d+)$', views.PlanContactsOperate.as_view()),
    url(r'^plan/load_pdf/(?P<pk>\d+)$', views.HtmlToPdf.as_view()),
    # url(r'^plan/contacts/add$', views.PlanContactsAdd.as_view()),
    # url(r'^img/upload$', views.UploadImg.as_view()),


    url(r'^sm$', views.SmWordView.as_view()),
    url(r'^sm/dts$', views.SmList.as_view()),
    url(r'^sm/(?P<id>\d+)$', views.SmWordView.as_view()),
    # SM词库管理---工作日设置
    url(r'^workdaylist$', views.WorkdayList.as_view()),
    url(r'^workdayedit$', views.WorkdayEdit.as_view()),
    url(r'^workdaysave$', views.WorkdaySave.as_view()),

    # 安全规则
    url(r'^group_rule$', views.GroupRuleView.as_view()),
    url(r'^group_rule/dts$', views.GroupRuleList.as_view()),
    url(r'^group_rule/(?P<id>\d+)$', views.GroupRuleView.as_view()),
    url(r'^alarm_rule$', views.AlarmRuleView.as_view()),
    url(r'^alarm_rule/dts$', views.AlarmRuleList.as_view()),
    url(r'^alarm_rule/(?P<id>\d+)$', views.AlarmRuleView.as_view()),
    url(r'^alarm_rule/start$', views.AlarmRuleStartView.as_view()),
    url(r'^alarm_rule/stop$', views.AlarmRuleStopView.as_view()),
    # 立即执行安全规则
    url(r'^alarm_rule/run$', views.AlarmRuleRunView.as_view()),
    # 事件类型
    url(r'^alarm_rule/event_type$', views.AlarmRuleEventTypeView.as_view()),

    # 告警事件
    # 告警类型
    url(r'^alarm_type$', views.AlarmTypeView.as_view()),
    # 告警监测
    url(r'^alarm_monitor$', views.AlarmMonitorView.as_view()),
    # 告警源
    url(r'^alarm_source$', views.AlarmSourceView.as_view()),
    # 告警趋势
    url(r'^alarm_trend$', views.AlarmTrendView.as_view()),
    # 告警列表
    url(r'^alarm_list/dts$', views.AlarmListView.as_view()),

    # 关闭告警日志
    url(r'^alarm_log/stop$', views.AlarmLogStopView.as_view()),
    # 告警日志列表
    url(r'^alarm_log/dts$', views.AlarmLogView.as_view()),
)
