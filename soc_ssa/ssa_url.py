# coding: utf-8
from django.conf.urls import patterns, url, include
from soc_ssa import views

api_urlpatterns = patterns(
    '',
    # Examples:
    # 全局态势

    url(r'^global/security_overview$', views.GlobalSecurityOverview.as_view()),  # 安全总览
    url(r'^global/danger_rating$', views.GlobaldangerRating.as_view()),  # 危险等级比例
    url(r'^global/situation_trend$', views.GlobalSituationTrend.as_view()),  # 全网态势发展趋势
    url(r'^global/hole_count$', views.GlobalHoleCount.as_view()),  # 漏洞统计
    url(r'^global/loophole_top5$', views.GlobalLoopholeTop5.as_view()),  # 最新重大漏洞TOP5
    url(r'^global/attack_num$', views.GlobalAttackNum.as_view()),  # 攻击次数
    url(r'^global/attack_source_total$', views.GlobalAttackSourceTotal.as_view()),  # 攻击来源
    url(r'^global/worm_num$', views.GlobalWormNum.as_view()),  # 蠕虫感染总数
    url(r'^global/assets_overview$', views.GlobalAssetsOverview.as_view()),  # 资产总览
    url(r'^global/assets_risk$', views.SourceHoleRating.as_view()),  # 资产风险占比  同 以下  漏洞严重级别
    url(r'^global/attack_rating$', views.GlobalAttackRating.as_view()),  # 攻击严重比例

    # 资源态势
    url(r'^source/hole$', views.SourceHole.as_view()),  # 漏洞统计"""
    url(r'^source/hole_rating$', views.SourceHoleRating.as_view()),  # 漏洞严重级别
    url(r'^source/hole_class$', views.SourceHoleClass.as_view()),  # 漏洞类别
    url(r'^source/bighole_top5$', views.GlobalLoopholeTop5.as_view()),  # 最新重大漏洞TOP5 和 全局态势里一样
    url(r'^source/business_risk$', views.SourceBusinessRisk.as_view()),  # 风险业务网站统计
    url(r'^source/weak$', views.SourceWeak.as_view()),  # 主机弱口令统计
    url(r'^source/source_risk$', views.SourceSourceRisk.as_view()),  # 资产和风险分布

    # 业务态势
    url(r'^business/visit_count$', views.BusinessVisitCount.as_view()),  # 当前访问人数
    url(r'^business/visit_top10$', views.BusinessVisitTop10.as_view()),  # 最近访问IP TOP10
    url(r'^business/server_status$', views.BusinessServerStatus.as_view()),  # 服务器响应状态占比
    url(r'^business/visit_trend$', views.BusinessVisitTrend.as_view()),  # 访问趋势
    url(r'^business/flow_trend$', views.BusinessFlowTrend.as_view()),  # 流量趋势
    url(r'^business/visit_location$', views.BusinessVisitLocation.as_view()),  # 访问地理位置
    url(r'^business/visit_os$', views.BusinessVisitOS.as_view()),  # 访问系统占比
    url(r'^business/visit_browser$', views.BusinessVisitBrowser.as_view()),  # 访问浏览器占比
    url(r'^websocket/business/visit_map$', views.business_visit_map),  # 访问数据
    url(r'^websocket/business/visit_people$', views.business_visit_people),  # 当前访问人数

    # 安全态势
    url(r'^security/trend$', views.SecurityTrend.as_view()),  # 攻击事件数发展趋势/蠕虫感染数量趋势
    url(r'^security/attack_top5$', views.SecurityAttackTop5.as_view()),  # 攻击目标IP地址top5/攻击单位top5
    # url(r'^security/attack_event_level$', views.SecurityAttackEventLevel.as_view()),  # 攻击事件等级占比
    url(r'^security/attack_event_level$', views.GlobalAttackNum.as_view()),  # 攻击事件等级占比
    url(r'^security/unusual_flow$', views.SecurityUnusualFlow.as_view()),  # 异常流量7日峰值
    url(r'^security/worm_top5$', views.SecurityWormTop5.as_view()),  # 蠕虫感染top5
    url(r'^security/serious_worm_top5$', views.SecuritySeriousWormTop5.as_view()),  # 严重蠕虫top5
    url(r'^security/attack_event_top24$', views.SecurityAttackEventTop24.as_view()),
    url(r'^websocket/security/attack_map$', views.attack_map),
    # 最近24小时攻击事件数

    # 新全局态势
    url(r'^new_global/risk_state$', views.RiskState.as_view()),  # 风险状态
    url(r'^new_global/score$', views.OverallScore.as_view()),  # 安全评分
    url(r'^new_global/event_count$', views.EventCount.as_view()),  # 事件统计
    url(r'^new_global/event_type_score$', views.EventTypeScore.as_view()),  # 设备风险指数比例
    url(r'^new_global/assets_event_trend$', views.AssetsEventTrend.as_view()),  # 事件趋势
    url(r'^new_global/event_risk_top$', views.EventRiskTop5.as_view()),  # 风险事件TOP5
    url(r'^new_global/foul_type_count$', views.FoulTypeCount.as_view()),  # 违规类型统计
    url(r'^new_global/virus_type_count$', views.VirusTypeCount.as_view()),  # 病毒类型统计
    url(r'^new_global/attack_type_count$', views.AttackTypeCount.as_view()),  # 攻击类型统计
    url(r'^new_global/asset_risk_top$', views.AssetRiskTop5.as_view()),  # 风险资产TOP5
    url(r'^new_global/foul_org_count$', views.FoulOrgCount.as_view()),  # 违规单位统计TOP5
    url(r'^new_global/virus_count$', views.VirusCount.as_view()),  # 病毒统计TOP5
    url(r'^new_global/attack_srcip_count$', views.AttackSrcipCount.as_view()),  # 攻击源统计TOP5
    url(r'^new_global/network_flow$', views.NetworkFlow.as_view()),  # 网络流量
    url(r'^new_global/asset_status$', views.AssetStatus.as_view()),  # 设备状态
    url(r'^new_global/attack_dstip_count$', views.AttackDstipCount.as_view()),  # 被攻击终端统计TOP5

    url(r'^new_global/new_event$', views.NewEvent.as_view()),  # 最新事件
    url(r'^new_global/terminal_level$', views.TerminalLevel.as_view()),  # 检查结果风险统计
    url(r'^new_global/terminal_foul_operate$', views.TerminalFoulOperate.as_view()),  # 终端操作违规
    url(r'^new_global/org_risk_count$', views.OrgRiskCount.as_view()),  # 部门风险统计
    url(r'^new_global/risk_ip_org$', views.RiskIpOrgCount.as_view()),  # 风险IP和风险部门数量统计
    url(r'^new_global/all_event_count$', views.AllEventCount.as_view()),  # 全局事件统计
)
