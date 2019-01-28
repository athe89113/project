# coding=utf8
import requests
import json
import datetime
import logging
import urllib2
from django.utils import timezone
from django.conf import settings
from soc_user.models import UserInfo
from soc.models import Message as ModelMessage
from django.contrib.auth.models import User
from django.core.cache import cache
# from soc_system.models import SetMsg, SetEmail
from soc_system.models import Message
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail

logger = logging.getLogger("soc")

WECHARTAPPID = ""
WECHARTAPPSECRET = ""
TEMPLATE = {}


class SendStationMessage(object):
    """站内信发送"""
    def __init__(self, type, target_id, agent_id, content):
        """
        
        :param type: 
        :param target_id: 
        :param agent_id: 
        :param content: 
        """
        self.type = type
        self.target_id = target_id
        self.agent_id = agent_id
        self.content = content

    def send(self):
        title = self.content.get("title")
        content = self.content.get("content")
        priority = self.content.get("priority", 3)
        the_type = self.type
        if self.agent_id == 0:
            # 站内
            user_id = self.target_id
        else:
            obj = UserInfo.objects.get(agent_id=self.agent_id, user__email=self.target_id)
            user_id = obj.user_id
        new_message = ModelMessage.objects.create(
            title=title,
            content=content,
            type=the_type,
            priority=priority,
            is_read=0,
            user_id=user_id
        )
        if new_message:
            return {'result': 'ok'}
        else:
            return {'result': 'error'}

# from soc_message_center.message_center.send_messages import SendEmail
class SendEmail(object):
    def __init__(self, content, agent_id,target_id=None, to=''):
        """
        发送邮件配置 
        :param target_id:  目标ID 若to参数有数据 以to为直接目标 否者以此user的email字段为目标发送邮件
        :param content:  neirong content = {"content":"this is a email","title":"the email title"}
        :param agent_id: 发送者的代理商ID
        :param to:  直接邮件目标，若为空 则以target_id为目标发送
        """
        self.target_id = target_id
        self.content = content
        self.agent_id = agent_id
        self.to = to

    def send(self):
        """
        发送邮件, 若用户 smtp 和cloud都有配置  先发cloud 若cloud发送失败 再发smtp
        :param
        :return: 
        """
        cloud = Message.objects.filter(agent_id=self.agent_id, type=4)
        smtp = Message.objects.filter(agent_id=self.agent_id, type=1)
        if cloud and smtp:
            email = SendEmailCloud(target_id=self.target_id, agent_id=self.agent_id, content=self.content, to=self.to)
            status = email.send()
            if status.get("result") != 'ok':
                email = SendEmailSMTP(target_id=self.target_id, agent_id=self.agent_id, content=self.content,
                                      to=self.to)
                return email.send()
            else:
                return status
        elif cloud:
            email = SendEmailCloud(target_id=self.target_id, agent_id=self.agent_id, content=self.content, to=self.to)
            return email.send()
        elif smtp:
            email = SendEmailSMTP(target_id=self.target_id, agent_id=self.agent_id, content=self.content,
                                  to=self.to)
            return email.send()
        else:
            return {"result": "error", "error": "配置错误"}


class SendMessage(object):
    """短信发送"""
    def __init__(self, content, agent_id, target_id=None, to='', sender_type_id=0, api='', api_user='', api_pwd=''):
        """
        :param target_id:  目标ID 要发送的对象的ID 获取手机号用 若to有值，则以to为直接目标
        :param sender_type_id: 一般等于等0 非0时候供外系统调用
        :param content:  内容 ={"content":"this is a test message"}
        :param agent_id: 发送者自己的代理商ID 用来获取短信服务器信息等
        :param to:  发送者手机号，若为空 调用target_id获取手机号 若不为空 直接用此手机号发送
        api api_user api_pwd 为可选参数 正常情况下是通过agent_id获取此三个信息，这里兼容测试用
        """

        self.target_id = target_id
        self.sender_type_id = sender_type_id
        self.content = content
        self.agent_id = agent_id
        self.to = to
        self.api = api
        self.api_user = api_user
        self.api_pwd = api_pwd

    def send_http_request(self, url):
        if not url:
            return 'error'
        req = urllib2.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16')
        try:
            response = urllib2.urlopen(req, timeout=3)
        except Exception, e:
            return e
        result = response.read()
        return result

    def send_phone_message(self, phone, content):
        """发送短信"""
        if not self.agent_id:
            url = self.api
            user = self.api_user
            pwd = self.api_pwd
        else:
            obj = Message.get_msg_info(agent_id=self.agent_id)
            url = obj.get("api")
            user = obj.get("user")
            pwd = obj.get("password")
        # url = settings.SEND_PHONE_MESSAGE_URL % (settings.CORP_ID, urllib2.quote(settings.CORP_PWD), phone, content)
        try:
            url = url % (user, urllib2.quote(pwd), phone, content)
        except:
            return {"result": "error", 'error': "发送失败"}
        # encoding gb2312
        url = url.encode('gb2312')
        status = self.send_http_request(urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
        try:
            code = status.split('<code>')[1].split('</code>')[0]
            if code == '03':
                logger.info("send message ok phone=%s content=%s "% (phone, content))
                return {"result": 'ok'}
            logger.warning("send message error phone=%s content=%s " % (phone, content))
            return {"result": "error", "error": "发送失败"}
        except Exception, e:
            logger.warning("send message error phone=%s content=%s " % (phone, content))
            return {"result": "error", "error": str(status)}

    def send(self):
        content = self.content.get("content")
        if self.to:
            return self.send_phone_message(self.to, content)
        else:
            if self.sender_type_id == 0:
                # 本系统的用户
                try:
                    userinfo = UserInfo.objects.get(user_id=self.target_id)
                except:
                    return {'result': 'error'}
                else:
                    phone = userinfo.phone
            else:
                # 外系统，要查代理商和email
                obj = UserInfo.objects.get(agent_id=self.sender_type_id, user__email=self.target_id)
                phone = obj.phone
            # return 1
            status = self.send_phone_message(phone, content)
            return status


class SendEmailSMTP(object):
    """                                         
    content = {"title":"sss", "content":"aaaaaa"}
    """

    def __init__(self, target_id, agent_id, content, sender_type_id=0, tls=False, ssl=False, send_address='', to='',
                 smtp_server='', smtp_user='', smtp_pwd='', ):
        """
        :param target_id:  如果to有值 以to为准备 如果to为空 以target_id为准
        :param agent_id:   若为空 用传入tls ssl smtp_server等数据发送 若有值 从数据库取配置
        :param content: 
        :param sender_type_id: 
        :param tls: 
        :param ssl: 
        :param send_address: 
        :param to: 
        :param smtp_server: 
        :param smtp_user: 
        :param smtp_pwd: 
        """
        self.target_id = target_id
        self.agent_id = agent_id
        self.content = content
        self.sender_type_id = sender_type_id
        self.tls = tls
        self.ssl = ssl
        self.send_address = send_address
        self.to = to
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_pwd = smtp_pwd

    def soc_send_email(self, title, content, host, username, password, use_tls, use_ssl, send_address, to):
        """
        :param title:  标题
        :param content:     内容
        :param host:    服务器
        :param username:    用户名
        :param password:    密码
        :param use_tls:     tls加密
        :param use_ssl:     ssl加密
        :param send_address:    发件人 一般和用户名一致
        :param to:  收件人
        :return: 
        构造一个smtp 然后发送邮件
        返回的status不为0则为成功
        """
        try:
            port = 25
            if int(use_ssl):
                port = 465
            smtp = EmailBackend(host=host, username=username,
                                password=password, use_ssl=bool(int(use_ssl)), use_tls=bool(int(use_tls)), port=port)
            status = send_mail(title, content, send_address,
                               [to], fail_silently=False, auth_user=username,
                               auth_password=password, connection=smtp)
            logger.info("send email success  to %s content=%s" % (to, content))
            return status, 'ok'
        except Exception, e:
            logger.warning("send email error  to %s content=%s, errors=%s" % (to, content, str(e)))
            return 0, '发送错误'

    def send(self):
        if self.to:
            email = self.to
        else:
            if self.sender_type_id == 0:
                # 站内的 target_id是一个用户ID
                user = User.objects.get(id=self.target_id)
                email = user.email
            else:
                # target_id是一个email
                email = self.target_id
        if self.agent_id:
            obj = Message.get_smtp_info(agent_id=self.agent_id)
            host = obj.get("smtp_server")
            username = obj.get("user")
            password = obj.get("password")
            tls_or_ssl = obj.get("tls_or_ssl")
            if not int(tls_or_ssl):
                use_tls = True
                use_ssl = False
            else:
                use_tls = False
                use_ssl = True
            send_address = obj.get("send_sender")
        else:
            host = self.smtp_server
            username = self.smtp_user
            password = self.smtp_pwd
            use_ssl = self.ssl
            use_tls = self.tls
            send_address = self.send_address

        status = self.soc_send_email(self.content["title"], self.content["content"], host, username, password, use_tls,
                                     use_ssl, send_address, email)
        return status


class SendEmailCloud(object):
    """
    搜狐邮件发送
    type  在这里暂时无用
    target_id = 发送对象的ID 

    content = 
        {
            "title":"the email title",
            "content":"the email content"
        }
    """
    def __init__(self, target_id, agent_id, content, sender_type_id=0, to='', api_user='', api_key=''):
        """
        :param target_id: 要发送对象的ID 如果 to有值，则忽以to为直接目标 略此target_id
        :param sender_type_id:  一般情况为0 表示站内 使用 为其他值表示跨站使用 (已经弃用)
        :param agent_id:  发送者的代理商ID 若为空则直接取api_user 和api_key的值
        :param content:  要发送的邮件 包含标题和内容 content = {"title":"","content":""}
        :param to: 要发送的直接目标，to有值，则忽以to为直接目标 略此target_id 若to为空 则以target_id为目标去取email
        :param api_user:  
        :param api_key: 
        """
        self.target_id = target_id
        self.sender_type_id = sender_type_id
        self.content = content
        self.agent_id = agent_id
        self.to = to
        self.api_user = api_user
        self.api_key = api_key

    def send(self):
        if self.to:
            email = self.to
        else:
            if self.sender_type_id == 0:
                # 站内的 target_id是一个用户ID
                user = User.objects.get(id=self.target_id)
                email = user.email
            else:
                # target_id是一个email
                email = self.target_id
        url = settings.SOHU_EMAIL_URL
        send_from, send_from_name = ('donotreply@sendcloud.com', 'alarm')
        title = self.content.get("title")
        content = self.content.get("content")
        if self.agent_id:
            try:
                obj = Message.get_cloud_info(agent_id=self.agent_id)
                api_user = obj.get("user")
                api_key = obj.get("password")
            except:
                api_user = ''
                api_key = ''
        else:
            api_user = self.api_user
            api_key = self.api_key

        params = {"api_user": api_user,
                  "api_key": api_key,
                  "to": email,
                  "from": send_from,
                  "fromname": send_from_name,
                  "subject": title,
                  "html": content,
                  }
        logger.info("send a email to %s, title=%s content=%s" % (email, title, content))
        status = requests.post(url, data=params)
        logger.info(status.text)
        status = json.loads(status.text)
        if status["message"] == 'success':
            logger.info("send email ok")
            return {'result': 'ok'}
        else:
            logger.warning("send email error %s" % (str(status["errors"])))
            return {'result': 'error'}


class SendWeChart(object):
    """"
    {
  "type":"登陆消息发送"  #发送者
  "target_id":46       #接受者
  "user":0             #发送方
  "content":  {
              "title":"xxxx",
              "content":"xxxx",
              "starttime":"xxxx",
              "endtime":"xxxx",
              "sender":"xxxx"
              "error_code":"xxxx"
              ......
              }
}
    """
    def __init__(self, send_data):
        self.type = send_data.get("type")
        self.target_id = send_data.get("target_id")
        self.sender_type_id = send_data.get("sender_type_id")
        self.content = send_data.get("content")

    def get_access_token_from_wechart(self):
        """
        从接口获取access_token 存入数据库 数据库只存一条数据 即ID为1的 有就覆盖 对于第一次就创建
        :return: 
        """
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" \
              % (WECHARTAPPID, WECHARTAPPSECRET)
        obj = requests.get(url)
        if obj.status_code == 200:
            get_data = json.loads(obj.text)
            # {"access_token":"ACCESS_TOKEN","expires_in":7200}
            if "access_token" in get_data:
                expires_in = get_data.get("expires_in", 0) - 60 * 5
                # 减五分钟作为缓冲时间,数据库里存的是UTC时间
                endtime = timezone.now() + datetime.timedelta(seconds=expires_in)
                # 把之前存数据库的数据存缓存
                cache_data = {
                    "token": get_data.get("access_token"),
                    "endtime": endtime
                }
                cache.set('wechart_token', cache_data, 2*60*60)
                """
                obj = WeChartToken.objects.filter(id=1).last()
                if obj:
                    obj.token = get_data.get("access_token")
                    obj.endtime = endtime
                    obj.save()
                else:
                    WeChartToken.objects.create(
                        id=1,
                        token=get_data.get("access_token"),
                        endtime=endtime
                    )
                """
                # print(get_data.get("access_token"))
                return get_data.get("access_token")
            else:
                # {"errcode": 40013, "errmsg": "invalid appid"}
                error_message = "get wechart access_token error! errcode: %s, errmsg: %s" \
                                % (get_data.get("errcode"), get_data.get("errmsg"))
                logger.warning(error_message)
                return False

    def get_access_token(self):
        """
        从数据库读数据，若过期，就调用接口获取数据
        :return: 
        """
        obj = cache.get('wechart_token')
        # obj = WeChartToken.objects.all().last()
        now = timezone.now()
        if obj and obj.endtime > now:
            # 如果时间未过期，直接用数据库里的token,如果过期，重新取一次。
            return obj.token
        else:
            token = self.get_access_token_from_wechart()
            if token:
                return token
            return 0

    def get_wechart_user(self, user_id):
        """
        从数据库查询相关用户的wechart唯一号
        :param user_id: 
        :return: 
        """
        try:
            obj = UserInfo.objects.get(user_id=user_id)
            return obj.wechart_unionid
        except Exception as e:
            return ""
        # return "oB8Zf1LVpItOL1H_D0viagXVKINQ"

    def get_wechart_user_email(self, sender_type_id, email):
        """
        从数据库查询相关用户的wechart唯一号
        """
        try:
            obj = UserInfo.objects.get(agent_id=sender_type_id, user__email=email)
            return obj.wechart_unionid
        except Exception as e:
            return ""
        # return "oB8Zf1LVpItOL1H_D0viagXVKINQ"

    def send_wechart_message(self, send_data):
        """
        发送微信消息函数
        """
        token = self.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + token
        obj = requests.post(url, data=json.dumps(send_data))
        if obj.status_code == 200:
            get_data = json.loads(obj.text)
            if get_data.get("errcode") == 0:
                return {'result': 'ok'}
        return {'result': 'error'}

    def send(self):
        if self.sender_type_id == 0:
            # 本系统的用户
            touser = self.get_wechart_user(self.target_id)
        else:
            touser = self.get_wechart_user_email(self.sender_type_id, self.target_id)
            # 外系统的用户，外系统绑定的时候存储
        template_id = TEMPLATE[self.type]
        send_data = {}
        if self.type == 1:
            # data = {
            #   "first":故障通知抬头，
            #   "performance":故障现象正文,
            #   "time":故障发生时间,
            #   "remark":结尾语句，
            # }
            # 故障通报通知 {{first.DATA}} 故障现象：{{performance.DATA}} 故障时间：{{time.DATA}} {{remark.DATA}}
            send_data = {
                "touser": touser,
                "template_id": template_id,
                "topcolor": "#FF0000",
                "data": {
                    "first": {
                        "value": self.content.get("first"),
                        "color": "#173177"
                    },
                    "performance": {
                        "value": self.content.get("performance"),
                        "color": "#173177"
                    },
                    "time": {
                        "value": self.content.get("time"),
                        "color": "#173177"
                    },
                    "remark": {
                        "value": self.content.get("remark"),
                        "color": "#173177"
                    }
                }
            }
        elif self.type == 2:
            # data = {
            #   "first": 消息抬头，
            #   "keyword1": 订单商品名称
            #   "keyword2": 订单编号
            #   "keyword3": 支付现金
            #   "keyword4": 支付时间
            #   "remark": 结尾语句
            # }
            # 订单支付成功通知
            # {{first.DATA}} 订单商品：{{keyword1.DATA}} 订单编号：{{keyword2.DATA}}
            # 支付金额：{{keyword3.DATA}} 支付时间：{{keyword4.DATA}} {{remark.DATA}}
            send_data = {
                "touser": touser,
                "template_id": template_id,
                "topcolor": "#FF0000",
                "data": {
                    "first": {
                        "value": self.content.get("first"),
                        "color": "#173177"
                    },
                    "keyword1": {
                        "value": self.content.get("keyword1"),
                        "color": "#173177"
                    },
                    "keyword2": {
                        "value": self.content.get("keyword2"),
                        "color": "#173177"
                    },
                    "keyword3": {
                        "value": self.content.get("keyword3"),
                        "color": "#173177"
                    },
                    "keyword4": {
                        "value": self.content.get("keyword4"),
                        "color": "#173177"
                    },
                    "remark": {
                        "value": self.content.get("remark"),
                        "color": "#173177"
                    }
                }
            }
        elif self.type == 3:
            # data = {
            #    "first":消息抬头,
            #    "keyword1":登录名，
            #    "keyword2":登录城市
            #    "keyword3":登录时间
            # }
            # 账号登录异常提醒   {{first.DATA}} 登录名：{{keyword1.DATA}} 登录城市：{{keyword2.DATA}}
            # 登录时间：{{keyword3.DATA}} {{remark.DATA}}
            send_data = {
                "touser": touser,
                "template_id": template_id,
                "topcolor": "#FF0000",
                "data": {
                    "first": {
                        "value": self.content.get("first"),
                        "color": "#173177"
                    },
                    "keyword1": {
                        "value": self.content.get("keyword1"),
                        "color": "#173177"
                    },
                    "keyword2": {
                        "value": self.content.get("keyword2"),
                        "color": "#173177"
                    },
                    "keyword3": {
                        "value": self.content.get("keyword3"),
                        "color": "#173177"
                    },
                    "keyword4": {
                        "value": self.content.get("keyword4"),
                        "color": "#173177"
                    },
                    "remark": {
                        "value": self.content.get("remark"),
                        "color": "#173177"
                    }
                }
            }
        return self.send_wechart_message(send_data)

