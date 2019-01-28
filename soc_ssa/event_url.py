# coding: utf-8
from django.conf.urls import patterns, url, include
from soc_ssa import views

api_urlpatterns = patterns(
    '',
    # Examples:
    # 事件搜索
    url(r'^select/list$', views.SelectFilterSelect2.as_view()),
    # 查询所有的数据标签以及数据量
    url(r'^tags/list$', views.ETLDataTagSelect2.as_view()),
    url(r'^search/line$', views.SSAEventSearchLine.as_view()),
    url(r'^search/dts$', views.SSAEventSearchDts.as_view()),
    url(r'^search/value_percent$$', views.SSAEventSearchValuePercent.as_view()),

    url(r'^analysis_field_map$', views.SecFieldMapList.as_view()),
    # 事件表字段
    url(r'^analysis_select/list$', views.SecSelectFilterSelect2.as_view()),
    # 事件搜索查询条件字段
    url(r'^analysis_select_search/list$', views.SecSelectFilterSearch.as_view()),
    # 事件来源
    url(r'^analysis_tags/list$', views.SECDataTagSelect2.as_view()),
    # 事件类型
    url(r'^analysis_type_tags/list$', views.SECDataSecTypeTagSelect2.as_view()),
    # # 二级事件类型
    # url(r'^analysis_second_type_tags/list$', views.SECDataSecTypeTagSelect2.as_view()),
    # 事件搜索图表
    url(r'^analysis_search/line$', views.SecEventSearchLine.as_view()),
    # 事件查询
    url(r'^analysis_search/dts$', views.SecEventSearchDts.as_view()),
    url(r'^analysis_search/value_percent$', views.SecEventSearchValuePercent.as_view()),

    # 事件时间线
    # url(r'^event_timeline/dts$', views.EventTimeLineDts.as_view()),
    # 事件时间线详情
    url(r'^event_timeline_info$', views.EventTimeLineInfo.as_view()),
    # IP风险值
    url(r'^ip_score_line$', views.IpScoreLine.as_view()),
    url(r'^event_ip$', views.EventIpDetail.as_view()),
    url(r'^event_ip/list$', views.EventIpList.as_view()),
    url(r'^event_ip_report$', views.IpEventReport.as_view()),

    # 固定参数
    url(r'^select_param/list$', views.SelectParamSelect2.as_view()),
    # 查询漏洞情况
    url(r'^select_vul_store', views.SelectVulStore.as_view()),
)
