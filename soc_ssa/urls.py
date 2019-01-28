# coding: utf-8
from django.conf.urls import patterns, url, include
from soc_ssa import views
from soc_ssa import ssa_url, event_url

urlpatterns = patterns(
    '',

    # 专家分析 管理SQL
    url(r'^rule_manage$', views.RuleManageList.as_view()),
    url(r'^rule_manage/(?P<pk>\d+)$', views.RuleManageDetail.as_view()),
    # 执行SQL
    url(r'^rule_manage/execute/dts$', views.ExecuteRuleDts.as_view()),

    # 数据管理
    url(r'^file_manage$', views.FileList.as_view()),
    url(r'^file_manage/dts$', views.FileListDts.as_view()),
    url(r'^file_manage/download$', views.FileDownload.as_view()),
    url(r'^file_manage/preview/dts$', views.FilePreiewDts.as_view()),
    # 报告管理
    url(r'^report/cell$', views.ReportCellList.as_view()),
    url(r'^report/cell/type$', views.ReportCellTypeList.as_view()),
    url(r'^report/cell/list$', views.ReportCellSelect2List.as_view()),
    url(r'^report/template$', views.ReportTemplateList.as_view()),
    url(r'^report/template/(?P<pk>\d+)$', views.ReportTemplateDetail.as_view()),
    url(r'^report/template/dts$', views.ReportTemplateDts.as_view()),
    url(r'^report/result/dts$', views.ReportResultDts.as_view()),
    url(r'^report/result/(?P<pk>\d+)$', views.ReportResultDetail.as_view()),
    url(r'^report/download/(?P<type>.+)/(?P<pk>\d+)$', views.report_download),
    url(r'^report/task/(?P<pk>\d+)/run$', views.TaskStart.as_view()),

    url(r'^alarm/(?P<conf_type>\d+)$', views.SSAAlarmConfDetail.as_view()),

    # 事件搜索
    url(r'^field_map$', views.FieldMapList.as_view()),
    # DashBorad
    url(r'^chart/perview$', views.SSAChartPerview.as_view()),
    url(r'^chart$', views.SSAChartList.as_view()),
    url(r'^chart/(?P<pk>\d+)$', views.SSAChartDetail.as_view()),
    url(r'^chart/dts$', views.SSAChartDts.as_view()),

    #
    url(r'^dashborad/chart$', views.SSADashBoradChart.as_view()),
    url(r'^dashborad$', views.SSADashBorad.as_view()),

    url(r'^event/', include(event_url.api_urlpatterns)),

    # 数据展示
    url(r'^', include(ssa_url.api_urlpatterns)),

)
