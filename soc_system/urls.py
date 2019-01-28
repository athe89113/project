# coding: utf-8
from django.conf.urls import patterns, url
from soc_system import views


urlpatterns = patterns(
    '',
    url(r'^version$', views.SystemVersion.as_view()),
    # 级联管理
    url(r'^nodes$', views.SystemNodeList.as_view()),
    url(r'^nodes/(?P<node_id>\d+)$', views.SystemNodeDetail.as_view()),
    # 中心状态刷新
    url(r'^nodes/(?P<node_id>\d+)/refresh$', views.SystemNodeStatusRefresh.as_view()),
    # 本机角色
    url(r'^nodes/self$', views.SystemNodeSelfDetail.as_view()),
    # 清除上下级节点
    url(r'^nodes/clear$', views.SystemNodeClear.as_view()),
    url(r'^nodes/clear/api$', views.SystemNodeClearApi.as_view()),
    url(r'^nodes/clear/api/parent$', views.SystemNodeClearApiParent.as_view()),

    url(r'^nodes/clear/status$', views.SystemNodeClearStatus.as_view()),
    # 中心认证，上级级联下级
    url(r'^nodes/auth$', views.SystemNodeAuth.as_view()),
    # 级联拓扑(显示上级中心)
    url(r'^nodes/topo$', views.SystemNodeTopo.as_view()),
    # 级联树状拓扑(从当前中心开始，不显示上级中心)
    url(r'^nodes/tree$', views.SystemNodeTree.as_view()),
    # 获取中心组件列表
    url(r'^nodes/components$', views.SystemNodeComponents.as_view()),
    url(r'^nodes/with_component$', views.SystemNodeWithComponents.as_view()),
    # 获取中心下的子中心的组件列表
    url(r'^nodes/children/components$', views.SystemNodeChildrenComponents.as_view()),
    # 查看上级中心状态
    url(r'^nodes/p_status$', views.SystemNodeParentStatus.as_view()),
    # 菜单管理
    url(r'^menus/(?P<menu_id>\d+)$', views.MenuDetail.as_view()),
    url(r'^menus/(?P<menu_id>\d+)/status$', views.MenuDetailUnlimited.as_view()),
    url(r'^menus/(?P<menu_id>\d+)/landing$', views.MenuDetailUnlimited.as_view()),
    url(r'^menus$', views.MenuList.as_view()),
    # 基本信息
    url(r'^baseinfo$', views.BaseInfo.as_view()),
    # 邮件管理
    url(r'^smtp_info$', views.SMTPinfo.as_view()),
    url(r'^smtp_info/test$', views.SendTestSmtp.as_view()),
    url(r'^cloud_email$', views.CloudEmail.as_view()),
    url(r'^cloud_email/send$', views.SendTestCloud.as_view()),
    # 短信发送
    url(r'^message$', views.Message.as_view()),
    url(r'^message/send$', views.MessageTest.as_view()),
    # 财务设置
    url(r'^finance$', views.Finance.as_view()),
    url(r'^paytest$', views.PayTest.as_view()),
    url(r'^order_callback$', views.AliPayCallBack.as_view()),  # 测试支付回调接口
    # 接口设置
    url(r'^qs_api$', views.SetApi.as_view()),
    # 接口测试
    url(r'^qs_api/test$', views.TestApi.as_view()),
    # 系统资源
    url(r'^monitor$', views.MonitorView.as_view()),
    url(r'^monitor/all$', views.MonitorViewAll.as_view()),
    # 系统健康
    url(r'^sys_status$', views.SysStatusView.as_view()),

    # 系统升级管理
    # 文件上传
    url(r'^upgrade/file/upload$', views.SystemUpgradeFileUpload.as_view()),
    # 上传和解析状态
    url(r'^upgrade/progress$', views.SystemUpgradeProgress.as_view()),
    # 中心升级列表，结构及状态
    url(r'^upgrade/nodes$', views.SystemUpgradeNodes.as_view()),
    # 升级处理
    url(r'^upgrade$', views.SystemUpgradeList.as_view()),
    # 升级列表
    url(r'^upgrade/list$', views.SystemUpgradeList.as_view()),
    # 重试
    url(r'^upgrade/retry$', views.SystemUpgradeRetry.as_view()),

    # 访问设置
    url(r'^visit$', views.Visit.as_view()),
    # 系统安全
    url(r'^system_safe/dts$', views.SystemSafeDts.as_view()),
    url(r'^system_safe$', views.SystemSafe.as_view()),
    # 二次验证
    url(r'^two_validation$', views.TwoValidation.as_view()),

    # 备份数据
    url(r'^backup/data$', views.BackupData.as_view()),
    # 调用子中心API接口（用于级联接口打通）
    url(r'^children_api$', views.ChildrenAPIViews.as_view()),
)
