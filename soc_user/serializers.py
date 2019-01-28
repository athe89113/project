# coding:utf-8
import logging
from hashlib import md5
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from soc_user.models import UserInfo, Company, VerifyTmp, Roles
from soc.serializers import UserInfos
from rest_framework import serializers
from common import generate_google_url

from utils.message import PHONE_PREFIX
logger = logging.getLogger("soc")


class UserSerializer(serializers.Serializer, UserInfos):

    username = serializers.CharField(required=False, max_length=30, allow_null=False, allow_blank=False,
                                     error_messages={'invalid': "用户名错误", 'null': "用户名不能为空", "blank": "用户名不能为空"})
    password = serializers.CharField(required=False, min_length=8, max_length=64, allow_null=False, allow_blank=False,
                                     error_messages={'invalid': "密码错误", 'null': "密码不能为空", "blank": "密码不能为空",
                                                     "min_length": "密码长度不能小于8个字符", "max_length": "密码长度不能超过64个字符"})
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False,
                                   error_messages={'invalid': "邮箱错误", 'null': "邮箱不能为空", "blank": "邮箱不能为空"})
    # 手机号码
    phone = serializers.CharField(max_length=11, allow_null=True, allow_blank=True,
                                  error_messages={"invalid": "手机号码错误"})

    is_admin = serializers.IntegerField(required=False, default=0)
    is_locked = serializers.IntegerField(required=False, default=0)
    company_id = serializers.IntegerField(required=False, default=None)
    gs_status = serializers.IntegerField(required=False, default=None)
    employee_id = serializers.CharField(required=False, max_length=30, min_length=1, allow_null=True, allow_blank=True,
                                        error_messages={
                                            "max_length": "工号不能长于30字节",
                                            "min_length": "工号不能短于1字节",
                                        })
    # agent_id = serializers.IntegerField(allow_null=False)
    # role_type = serializers.IntegerField(allow_null=False,
    #                                      error_messages={"invalid": "错误", 'null': "角色不能为空", 'blank': '角色不能为空'})

    role_id = serializers.IntegerField(allow_null=True, required=False, default=None)

    def validate_role_id(self, data):
        if not data:
            return data
        try:
            role_obj = Roles.objects.get(id=data, agent=self.agent)
        except Roles.DoesNotExist:
            raise serializers.ValidationError("角色错误")
        return role_obj

    def validate_username(self, data):
        if not self.instance:
            if not data:
                raise serializers.ValidationError("用户名不能为空")
        if User.objects.filter(username=data).exists():
            # 用户名不能重复
            if self.instance:
                if User.objects.exclude(id=self.instance.id).filter(username=data).exists():
                    raise serializers.ValidationError("用户名已经注册")
            else:
                raise serializers.ValidationError("用户名已经注册")

        return data

    def validate_email(self, data):

        if User.objects.filter(email=data).exists():
            # 邮箱不能重复 => 验证时会有问题
            if self.instance:
                if User.objects.exclude(id=self.instance.id).filter(email=data).exists():
                    raise serializers.ValidationError("邮箱已经注册")
            else:
                raise serializers.ValidationError("邮箱已经注册")

        return data

    def validated_password(self, data):
        if not self.instance:
            if not data:
                raise serializers.ValidationError("密码不能为空")

    def validate_phone(self, phone):
        """
        验证手机号码段
        :param phone:
        :return:
        """
        if not phone:
            return phone
        if not self.instance:
            if UserInfo.objects.filter(phone=phone).exists():
                raise serializers.ValidationError("手机号码已经注册")
        else:
            if UserInfo.objects.exclude(user=self.instance).filter(phone=phone).exists():
                raise serializers.ValidationError("手机号码已经注册")

        supported = False
        for pre in PHONE_PREFIX:
            if phone.startswith(pre):
                supported = True
                break
        if not supported:
            logger.error('not supported phone: ' + phone)
            raise serializers.ValidationError('手机号码不支持')
        return phone

    def validate_employee_id(self, data):
        """
        验证手机号码段
        :param phone:
        :return:
        """
        if not data:
            return data
        if not self.instance:
            if UserInfo.objects.filter(employee_id=data, agent=self.agent).exists():
                raise serializers.ValidationError("工号不能重复")
        else:
            if UserInfo.objects.exclude(user=self.instance).filter(employee_id=data, agent=self.agent).exists():
                raise serializers.ValidationError("工号不能重复")
        return data

    def validate(self, attrs):
        request = self.context.get('request')
        is_locked = attrs.get('is_locked')
        company_id = attrs.get('company_id')
        role_obj = attrs.get('role_id')
        # 判断是否为注册
        if not hasattr(request, 'user'):
            role_type = 3
        else:
            role_type = request.user.userinfo.role_type
            if request.user.userinfo.is_admin:
                if request.user.userinfo.role_type == 3:
                    company_id = request.user.userinfo.company_id
            else:
                raise serializers.ValidationError("无权操作")
        if company_id:
            role_type = 3
        attrs['role_type'] = role_type
        attrs['company_id'] = company_id
        # 处理在注册时 没有request.user导致异常
        if getattr(request, 'user', ' AnonymousUser') == self.instance:
            if self.instance.userinfo.is_locked != is_locked:
                raise serializers.ValidationError("不能修改自己的状态")
            old_role = self.instance.userinfo.roles.first()
            if role_obj and (old_role != role_obj):
                raise serializers.ValidationError("不能修改自己的角色")

        return attrs

    def create(self, validated_data):
        role = validated_data.get('role_id')
        role_type = validated_data.get('role_type')
        is_admin = validated_data['is_admin']
        is_locked = validated_data['is_locked']
        username = validated_data['username']
        company_id = validated_data['company_id']
        employee_id = validated_data.get('employee_id')
        if role:
            if role.is_admin:
                is_admin = 1
            else:
                is_admin = 0
        else:
            if is_admin:
                role = Roles.objects.get(agent=self.agent, is_admin=1)
            else:
                role = Roles.objects.get(agent=self.agent, name='运维')

        user = User.objects.create_user(
            username=username,
            password=validated_data['password'],
            email=validated_data['email'],
        )
        if user:

            user_info = UserInfo.objects.create(user=user,
                                                company_id=company_id,
                                                is_admin=is_admin,
                                                phone=validated_data['phone'],
                                                agent_id=self.context.get('agent').id,
                                                employee_id=employee_id,
                                                role_type=role_type,
                                                is_locked=is_locked)
            gs_key, b32secret, url, _ = generate_google_url(username)
            user_info.google_secret = gs_key

            user_info.roles.add(role)
        return user

    def update(self, instance, validated_data):
        role_obj = validated_data.get("role_id")
        password = validated_data.get("password")
        gs_status = validated_data.get("gs_status")
        # 解绑二次验证
        if gs_status == 0:
            instance.userinfo.gs_status = 0
            instance.userinfo.google_secret = ''
        info = ''
        if validated_data.get("username", '') != instance.username:
            info = '用户名'
        if validated_data.get("phone", '') != instance.userinfo.phone:
            info = '手机'
        if validated_data.get("email", '') != instance.email:
            info = '邮箱'
        if validated_data.get("employee_id", '') != instance.userinfo.employee_id:
            info = '工号'
        if password:
            info = '密码'
        if validated_data.get("is_locked", '') != instance.userinfo.is_locked:
            info = '状态'
        if role_obj:
            role_ids = []
            for i in instance.userinfo.roles.values():
                role_ids.append(i.get('id'))
            if int(role_obj.id) not in role_ids:
                info = '角色'
        if password:
            self.instance.set_password(password)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.userinfo.employee_id = validated_data.get("employee_id", instance.userinfo.employee_id)
        instance.userinfo.phone = validated_data.get("phone", instance.userinfo.phone)
        instance.userinfo.is_locked = validated_data.get("is_locked", instance.userinfo.is_locked)
        if role_obj:
            instance.userinfo.is_admin = role_obj.is_admin
            instance.userinfo.roles.clear()
            instance.userinfo.roles.add(role_obj)
        instance.save()
        instance.userinfo.save()
        cache_key = "permission_cache_user_{0}".format(self.instance.id)
        cache.delete(cache_key)
        return instance, info


class CompanySerializer(serializers.Serializer):
    """
    公司序列化
    """

    name = serializers.CharField(required=True, max_length=120, allow_blank=False, allow_null=False,
                                 error_messages={'invalid': "公司名称错误", 'blank': '公司名称不能为空'})
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True, default='',
                                   error_messages={'invalid': "公司邮箱错误"})
    phone = serializers.CharField(max_length=11, allow_null=True, allow_blank=True, default='',
                                  error_messages={'invalid': "公司电话错误"})
    address = serializers.CharField(max_length=256, allow_null=True, default='',
                                    error_messages={'invalid': "公司电话错误"})

    def validate(self, attrs):

        if self.instance:
            # 更新时
            pass
        else:
            if Company.objects.filter(agent=self.context.get("agent"), name=attrs.get('name')).exists():
                raise serializers.ValidationError('公司名称重复')
        return attrs

    def create(self, validated_data):
        """
        创建公司
        :param validated_data:
        :return:
        """
        validated_data['agent'] = self.context.get("agent")
        company = Company.objects.create(**validated_data)
        return company

    def udpate(self, instance, validated_data):
        """
        更新公司
        :param instance:
        :param validated_data:
        :return:
        """
        instance.name = validated_data.get("name", instance.name)
        instance.save()


class PhoneCaptchaSerializer(serializers.Serializer):
    """
    手机验证
    """

    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False,
                                   error_messages={'invalid': "邮箱错误", "blank": "邮箱不能为空", 'null': '邮箱不能为空'})
    phone = serializers.CharField(max_length=11, allow_null=False, allow_blank=False,
                                  error_messages={'invalid': "手机号码错误", "blank": "手机号码不能为空", 'null': '手机号码不能为空'})

    def validate_phone(self, phone):
        """
        验证手机号码段
        :param phone:
        :return:
        """
        if UserInfo.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("手机号码已经注册")
        supported = False
        for pre in PHONE_PREFIX:
            if phone.startswith(pre):
                supported = True
                break
        if not supported:
            logger.error('not supported phone: ' + phone)
            raise serializers.ValidationError('手机号码不支持')
        return phone

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')

        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError('邮箱已经被注册')

        # todo 避免重复发送
        tmp = VerifyTmp.objects.filter(type=1, email=email, phone=phone).last()
        if tmp and tmp.expire_time > timezone.now():
            print("验证码未过期")
        return attrs

    def create(self, validated_data):
        # captcha 从外边传入
        email = validated_data['email']
        phone = validated_data['phone']
        # import pdb
        # pdb.set_trace()
        data = {
            "validated": 0,
            "expire_time": timezone.now()+timezone.timedelta(minutes=30),
            "captcha": md5(self.context.get('captcha')).hexdigest()
        }

        tmp = VerifyTmp.objects.update_or_create(email=email, phone=phone, type=1, defaults=data)
        return tmp


class EmailVerificationSerializer(serializers.Serializer):
    """
    邮箱验证
    """

    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False,
                                   error_messages={'invalid': "邮箱错误", "blank": "邮箱不能为空", 'null': '邮箱不能为空'})

    def validate(self, attrs):
        email = attrs.get('email')

        if not User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError('邮箱不存在')

        # todo 避免重复发送
        tmp = VerifyTmp.objects.filter(type=2, email=email, phone='').last()
        if tmp and tmp.expire_time > timezone.now():
            print("验证码未过期")
        return attrs

    def create(self, validated_data):
        # captcha 从外边传入
        email = validated_data['email']
        # import pdb
        # pdb.set_trace()
        data = {
            "validated": 0,
            "expire_time": timezone.now()+timezone.timedelta(minutes=30),
            "link_code": md5(self.context.get('link_code')).hexdigest()
        }

        tmp = VerifyTmp.objects.update_or_create(email=email, phone="", type=2, defaults=data)
        return tmp


class WorkTimeSerializers(serializers.Serializer):
    """
    工作时间
    """
    morning_start_time = serializers.DateTimeField(required=False, allow_null=False)
    morning_end_time = serializers.DateTimeField(required=False, allow_null=False)
    afternoon_start_time = serializers.DateTimeField(required=False, allow_null=False)
    afternoon_end_time = serializers.DateTimeField(required=False, allow_null=False)
