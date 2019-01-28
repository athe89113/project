# coding: utf-8

from django.conf.urls import patterns, url
from soc_user import views
from soc_user import select2_views

urlpatterns = patterns(
    '',
    # 登录
    url(r'^login$', views.Login.as_view()),
    url(r'^check_password$', views.CheckPassword.as_view()),
    url(r'^sso/login/(?P<base_str>.+)$', views.SSOLogin.as_view()),
    url(r'^logout$', views.Logout.as_view()),
    # 注册
    url(r'^register$', views.Register.as_view()),
    # 注册状态
    url(r'^register_status$', views.RegisterStatus.as_view()),
    url(r'^phone_captcha$', views.PhoneCaptcha.as_view()),
    # 找回密码
    url(r'^forgot_password$', views.ForgotPassword.as_view()),
    # 验证邮箱链接
    url(r'^confirm$', views.ConfirmEmail.as_view()),

    url(r'^user$', views.User.as_view()),
    url(r'^user/dts$', views.UserDataTableList.as_view()),
    url(r'^user/list$', select2_views.UserSelect2.as_view()),
    url(r'^user/(?P<user_id>\d+)$', views.User.as_view()),
    url(r'^user/(?P<user_id>\d+)/avatar$', views.AvatarView.as_view()),

    url(r'^admin/user$', views.AdminUser.as_view()),
    url(r'^admin/user/(?P<user_id>\d+)$', views.AdminUser.as_view()),

    url(r'^avatar$', views.AvatarView.as_view()),
    url(r'^profile$', views.CurrentUserProfile.as_view()),
    url(r'^user/two_factor$', views.UserTwoFactorQRcode.as_view()),

    # 代理商权限
    url(r'^perms$', views.Perms.as_view()),
    url(r'^agent_perms$', views.AgentPerms.as_view()),
    url(r'^work_group$', views.WorkGroup.as_view()),
    url(r'^work_group/(?P<wg_id>\d+)$', views.WorkGroup.as_view()),
    # url(r'user_list$', views.UserList.as_view()),

    url(r'^company$', views.CompanyList.as_view()),
    url(r'^company/(?P<id>\d+)$', views.CompanyDetail.as_view()),
    # select2
    url(r'^company/list$', views.CompanySelect2.as_view()),
    # 公司管理
    url(r'^company/dts', views.CompanyDataTableList.as_view()),

    # 工作时间
    url(r'^work_time$', views.WorkTimeView.as_view()),

)
