# coding=utf-8
import os
import json
import logging
from hashlib import md5
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.timezone import localtime
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from models import (VulStore, PlanStore, KnowledgeStore, SearchKnowledgeLog,
                    KnowledgeTag, KnowledgeType, SceneType, PlanTag, PlanContacts,
                    VulStoreVersion, SmWord, WorkDay, AlarmLog, AlarmRule, GroupRule)
from store_serializers import (KnowledgeSerializer as k_ser,
                               PlanSerializer as p_ser,
                               PlanContactsSerializer as c_ser,
                               SmWordSerializer as sm_ser, WorkDaySerializer,
                               GroupRuleSerializer as group_rule_ser,
                               AlarmRuleSerializer as alarm_rule_ser)
from soc_knowledge.knowledge_utils import get_level, get_data_source, get_firm_level
from soc_knowledge.create_pdf import render_pdf, create_pdf_file
from utils.datatable import DatatableView
from datetime import datetime
from utils import mysql_select, es_select

logger = logging.getLogger('task')


def return_instance_error(obj):
    """ 找不到对象的 错误信息
    :param obj:
    :return:
    """
    if not obj:
        return Response({
            "status": 500,
            "msg": u'查询不到信息',
            "error": u"查询不到信息"
        })


fmt = lambda dt: localtime(dt).strftime('%Y-%m-%d %H:%M:%S')


class VulLibraryList(DatatableView):
    """ 漏洞库列表
    """
    render_columns = [
        ("id", "id", 0),
        ("vul_nam", "vul_name"),
        ("publish_date", "publish_date", 0),
        ("vul_id", "vul_id"),
        ("vul_level", "vul_level", 0),
        ("vul_type", "vul_type", 0),
        ("attack_type", "attack_type", 0),
        ("description", "description")
    ]
    model = VulStore

    def get_initial_queryset(self):
        """获取可查询的数据"""
        req = self.request.data
        tag = req.get('tag')
        vul_list = VulStore.objects.all()
        if tag:
            pass
        start_date = req.get('start_date')
        if start_date:
            vul_list = vul_list.filter(publish_date__gte=start_date)
        end_date = req.get('end_date')
        if end_date:
            vul_list = vul_list.filter(publish_date__lte=end_date)
        data_source = req.get('data_source')
        if data_source:
            vul_list = vul_list.filter(data_source=data_source)
        return vul_list.order_by('-publish_date')

    def prepare_one_result(self, item, data_dict):
        """ 最后返回数据 处理
        :param item: 每条数据
        :param data_dict: 返回的数据
        :return:
        """
        data_dict['level'] = get_level(item)
        source_name = get_data_source(item.data_source)
        data_dict['source_name'] = source_name

        for i in data_dict:
            data_dict[i] = data_dict[i] if data_dict[i] else '--'
        return data_dict

    def prepare_results(self, qs):
        """
        格式化输出形式, 最终输出的 data(>1.10)/aaData
        """
        data = super(VulLibraryList, self).prepare_results(qs)
        # 处理搜索记录
        if self.request.data.get('search[value]'):
            search_list = []
            for k in qs[:6]:
                search_list.append(SearchKnowledgeLog(search_type=0, result_id=k.id))
            SearchKnowledgeLog.objects.bulk_create(search_list)
        return data


class VulDetail(APIView):
    """ 漏洞详情
    """

    def get(self, request, pk):
        """ 详情信息
        """
        vul_obj = VulStore.objects.filter(pk=pk).first()
        data = model_to_dict(vul_obj)
        data['user'] = ''
        data['range'] = ''
        data['suggest'] = ''
        for k in data:
            if not data[k]:
                data[k] = u'暂无'
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": data
        }
        return Response(context)


class QuickSearchVul(APIView):
    """ 快速搜索漏洞详情
    """

    def post(self, request):
        """ 快速条件搜索
        """
        parm = request.data
        vul_name = parm.get('vul_name')
        vul_id = parm.get('vul_id')
        start = parm.get('start_date')
        end = parm.get('end_date')
        vul_obj = VulStore.objects.all()
        if vul_name:
            vul_obj = vul_obj.filter(vul_name=vul_name)
        if vul_id:
            vul_obj = vul_obj.filter(vul_id=vul_id)
        if start:
            vul_obj = vul_obj.filter(publish_date__gte=start)
        if end:
            vul_obj = vul_obj.filter(publish_date__lte=end)

        vul_obj = vul_obj.first()
        if not vul_obj:
            context = {
                "status": 500,
                "msg": u'未查询到结果',
                "error": u'未查询到结果'
            }
            return Response(context)
        result = model_to_dict(vul_obj)
        result['user'] = ''
        result['range'] = ''
        result['suggest'] = ''
        for k in result:
            if not result[k]:
                result[k] = u'暂无'
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)


class SimilarVul(APIView):
    """ 相关漏洞列表
    """

    def get(self, request, tp):
        """ 相关漏洞列表
        """
        vul_list = VulStore.objects.filter(vul_type=tp).order_by('-publish_date')
        data_list = []

        for v in vul_list[:5]:
            level = get_level(v)
            data_list.append({
                'id': v.id,
                'vul_name': v.vul_name,
                'publish_date': v.publish_date,
                'vul_id': v.vul_id,
                'level': level
            })

        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": data_list
        }
        return Response(context)


class KnowledgeList(DatatableView):
    """ 知识库列表
    """
    render_columns = [
        ("id", "id", 0),
        ("title", "title"),
        ("update_time", "update_time", 0),
        ("type", "type__name", 0),
        ("content", "content")
    ]
    model = KnowledgeStore

    def get_initial_queryset(self):
        """获取可查询的数据"""
        req = self.request.data
        tag = req.get('tag')
        knowledge_list = KnowledgeStore.objects.all()
        if tag:
            tag_list = tag.split(',')
            knowledge_list = knowledge_list.filter(tag__name__in=tag_list)
        letter = req.get('letter')
        if letter:
            knowledge_list = knowledge_list.filter(search_letter=letter.upper())
        type = req.get('type')
        if type:
            knowledge_list = knowledge_list.filter(type__name=type)
        return knowledge_list

    def prepare_one_result(self, item, data_dict):
        """ 最后返回数据 处理
        :param item: 每条数据
        :param data_dict: 返回的数据
        :return:
        """
        tag_list = [i.name for i in item.tag.all()]
        data_dict['tag'] = tag_list
        data_dict['update_time'] = fmt(data_dict['update_time'])
        return data_dict

    def prepare_results(self, qs):
        """
        格式化输出形式, 最终输出的 data(>1.10)/aaData
        """
        data = super(KnowledgeList, self).prepare_results(qs)
        # 处理搜索记录
        if self.request.data.get('search[value]'):
            search_list = []
            for k in qs[:6]:
                search_list.append(SearchKnowledgeLog(search_type=1, result_id=k.id))
            if search_list:
                # 先清空搜索表
                SearchKnowledgeLog.objects.filter(search_type=1).delete()
            SearchKnowledgeLog.objects.bulk_create(search_list)
        return data


class KnowledgeAdd(APIView):
    """ 添加知识库
    """

    def post(self, request):
        """ 添加知识库
        """
        req = request.data
        tag = req.get('tag')
        tag_info = {"tag": tag}
        obj_serializer = k_ser(data=request.data, context=tag_info)
        if obj_serializer.is_valid():
            obj_serializer.save()
            context = {
                "status": 200,
                "msg": u'执行成功',
            }
        else:
            msg = u'执行失败'
            for error in obj_serializer.errors:
                msg = obj_serializer.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": msg
            }
        return Response(context)


class KnowledgeDetail(APIView):
    """ 知识库详情
    """

    def get_objects(self, pk):
        """ 获取对象
        """
        knowledge = KnowledgeStore.objects.filter(pk=pk).first()
        return knowledge

    def get(self, request, pk):
        """ 获取详情
        """
        knowledge = self.get_objects(pk)
        return_instance_error(knowledge)

        result = model_to_dict(knowledge, exclude=['tag', 'type'])
        result['tag'] = [k.name for k in knowledge.tag.all()]
        result['type'] = knowledge.type.name
        result['update_time'] = fmt(knowledge.update_time)
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)

    def put(self, request, pk):
        """ 修改 详情
        """
        knowledge = self.get_objects(pk)
        return_instance_error(knowledge)
        tag = request.data.get('tag')
        tag_info = {"tag": tag}
        obj_serializer = k_ser(instance=knowledge, data=request.data, context=tag_info)
        if obj_serializer.is_valid():
            obj_serializer.save()
            context = {
                "status": 200,
                "msg": u'执行成功',
            }
        else:
            msg = u'执行失败'
            for error in obj_serializer.errors:
                msg = obj_serializer.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": msg
            }
        return Response(context)

    def delete(self, request, pk):
        """ 删除详情
        """
        knowledge = self.get_objects(pk)
        return_instance_error(knowledge)
        knowledge.delete()
        context = {
            "status": 200,
            "msg": u'执行成功',
        }
        return Response(context)


class LastAddKnowledge(APIView):
    """ 最新添加知识库记录
    """

    def get(self, request):
        """ 最近添加知识库"""
        knowledge = KnowledgeStore.objects.values_list('title', 'create_time').order_by('-create_time')[:6]
        result = [{'title': k[0], 'create_time': fmt(k[1])} for k in knowledge]

        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)


class SimilarKnowledge(APIView):
    """ 相关知识库列表
    """

    def get(self, request, tp):
        knowledge = KnowledgeStore.objects.filter(type=tp).order_by('-create_time')[:6]
        result = [model_to_dict(k) for k in knowledge]
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)


class LastKnowledgeSearch(APIView):
    """ 最近的预案搜索
        是所有用户最近的搜索
    """

    def get(self, request):
        """ 最近的预案搜索
        """
        all_search = SearchKnowledgeLog.objects.filter(search_type=1).order_by('-search_time')[:6]
        result = dict()
        for s in all_search:
            result[s.id] = {'result_id': s.result_id, 'search_time': fmt(s.search_time)}

        last_knowledge = KnowledgeStore.objects.filter(
            id__in=[i['result_id'] for i in result.values()])
        k_data = dict()
        for p in last_knowledge:
            k_data[p.id] = p.title
        data = []
        for k in result.values():
            name = k_data.get(k['result_id'])
            if not name:
                continue
            data.append({
                'id': k['result_id'],
                'name': name,
                'search_time': k['search_time']})

        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": data
        }
        return Response(context)


class PlanList(DatatableView):
    """ 预案库列表
    """
    render_columns = [
        ("id", "id", 0),
        ("title", "title"),
        ("user", "user", 0),
        ("update_time", "update_time", 0),
        ("level", "level", 0),
        ("brief", "brief")
    ]
    model = PlanStore

    def get_initial_queryset(self):
        """获取可查询的数据"""
        req = self.request.data
        tag = req.get('tag')
        plan_list = PlanStore.objects.all()
        if tag:
            tag_list = tag.split(',')
            plan_list = plan_list.filter(tag__name__in=tag_list)
        level = req.get('level')
        if level:
            plan_list = plan_list.filter(level=level)
        return plan_list

    def prepare_one_result(self, item, data_dict):
        """ 最后返回数据 处理
        :param item: 每条数据
        :param data_dict: 返回的数据
        :return:
        """
        tag_list = [i.name for i in item.tag.all()]
        data_dict['tag'] = tag_list
        data_dict['update_time'] = fmt(data_dict['update_time'])
        return data_dict

    def prepare_results(self, qs):
        """
        格式化输出形式, 最终输出的 data(>1.10)/aaData
        """
        data = super(PlanList, self).prepare_results(qs)
        # 处理搜索记录
        if self.request.data.get('search[value]'):
            search_list = []
            for k in qs[:6]:
                search_list.append(SearchKnowledgeLog(search_type=2, result_id=k.id))
            if search_list:
                # 先清空搜索表
                SearchKnowledgeLog.objects.filter(search_type=2).delete()
            SearchKnowledgeLog.objects.bulk_create(search_list)
        return data

    def ordering(self, qs):
        req = self.request.data
        sort_col = req.get('sort_col')
        sort = req.get('sort')
        if sort_col:
            if sort == 1:
                sort_col = '-' + sort_col
            qs = qs.order_by(sort_col)
        return qs


class LastAddPlan(APIView):
    """ 最新添加预案列表
    """

    def get(self, request):
        """最新添加预案列表
        """
        plan = PlanStore.objects.all().order_by('-create_time')[:6]
        result = []
        for k in plan:
            p_dict = dict()
            p_dict['id'] = k.id
            p_dict['title'] = k.title
            p_dict['level'] = k.level
            p_dict['create_time'] = fmt(k.create_time)
            result.append(p_dict)
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result

        }
        return Response(context)


class LastPlanSearch(APIView):
    """ 最近的预案搜索
    """

    def get(self, request):
        """最近的预案搜索"""
        all_search = SearchKnowledgeLog.objects.filter(search_type=2).order_by('-search_time')[:6]
        result = dict()
        for s in all_search:
            result[s.id] = {'result_id': s.result_id, 'search_time': fmt(s.search_time)}

        last_plan = PlanStore.objects.filter(
            id__in=[i['result_id'] for i in result.values()])
        k_data = dict()
        for p in last_plan:
            k_data[p.id] = [p.title, p.level]
        data = []
        for k in result.values():
            name = k_data.get(k['result_id'])
            if not name:
                continue
            data.append({
                'id': k['result_id'],
                'name': name[0],
                'level': name[1],
                'search_time': k['search_time']})
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": data
        }
        return Response(context)


class PlanAdd(APIView):
    """ 添加预案库
    """

    def post(self, request):
        """ 添加预案库
        """
        req = request.data
        # 标签 多标签，分割
        tag = req.get('tag')
        # 联系人 多联系人，分割
        contact = req.get('contact')
        info = {
            "tag": tag,
            "contact": contact
        }
        obj_serializer = p_ser(data=req, context=info)
        if obj_serializer.is_valid():
            obj_serializer.save()
            context = {
                "status": 200,
                "msg": u'执行成功',
            }
        else:
            msg = u'执行失败'
            for error in obj_serializer.errors:
                msg = obj_serializer.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": msg
            }
        return Response(context)


class PlanDetail(APIView):
    """ 预案详情
    """

    def get_objects(self, pk):
        """ 获取对象
        """
        plan = PlanStore.objects.filter(pk=pk).first()
        return plan

    def get(self, request, pk):
        """ 查询详情"""
        plan = self.get_objects(pk)
        return_instance_error(plan)

        result = model_to_dict(plan, exclude=['tag', ])
        result['tag'] = [k.name for k in plan.tag.all()]
        result['contact'] = [model_to_dict(p) for p in plan.plancontacts_set.all()]
        if not result['contact']:
            result['contact'] = [{'name': '--', 'phone': '--', 'email': '--'}]
        result['create_time'] = fmt(plan.create_time)
        result['update_time'] = fmt(plan.update_time)
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)

    def put(self, request, pk):
        """修改详情
        """
        plan = self.get_objects(pk)
        return_instance_error(plan)

        req = request.data
        # 标签 多标签，分割
        tag = req.get('tag')
        # 联系人 多联系人，分割
        contact = req.get('contact')
        info = {
            "tag": tag,
            "contact": contact
        }
        obj_serializer = p_ser(instance=plan, data=req, context=info)
        if obj_serializer.is_valid():
            obj_serializer.save()
            context = {
                "status": 200,
                "msg": u'执行成功',
            }
        else:
            msg = u'执行失败'
            for error in obj_serializer.errors:
                msg = obj_serializer.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": msg
            }
        return Response(context)

    def delete(self, request, pk):
        """删除
        """
        plan = self.get_objects(pk)
        return_instance_error(plan)
        plan.delete()
        context = {
            "status": 200,
            "msg": u'执行成功',
        }
        return Response(context)


class KnowledgeAttrList(APIView):
    """ 知识库标签列表
    """

    def get(self, request):
        """ 知识库类型标签
        """
        tag_list = KnowledgeTag.objects.all()
        data = {'tag': [], 'type': [], 'scene': []}
        for t in tag_list:
            data['tag'].append(t.name)
        type_list = KnowledgeType.objects.all()
        for k in type_list:
            data['type'].append(k.name)
        scene_list = SceneType.objects.all()
        for s in scene_list:
            data['scene'].append(s.name)
        context = {
            "status": 200,
            "msg": u'执行成功',
            "data": data
        }
        return Response(context)


class PlanAttrList(APIView):
    """ 知识库标签列表
    """

    def get(self, request):
        """ 预案库标签
        """
        tag_list = PlanTag.objects.all()
        data = {'tag': [], 'level': [1, 2, 3, 4], 'scene': []}
        for t in tag_list:
            data['tag'].append(t.name)
        scene_list = SceneType.objects.all()
        for s in scene_list:
            data['scene'].append(s.name)
        context = {
            "status": 200,
            "msg": u'执行成功',
            "data": data
        }
        return Response(context)


class PlanHot(APIView):
    """ 热门预案
    """

    def get(self, request):
        """ 热门预案"""
        hot_plan = PlanStore.objects.filter(level=4).order_by('-update_time')[:6]
        data = []
        for p in hot_plan:
            info = dict()
            info['name'] = p.title + '(' + p.scene + ')'
            info['create_time'] = fmt(p.create_time)
            data.append(info)
        context = {
            "status": 200,
            "msg": u'执行成功',
            "data": data
        }
        return Response(context)


class PlanSimilar(APIView):
    """ 相关预案
    """

    def get(self, request, tp):
        """相关预案"""
        hot_plan = PlanStore.objects.filter(scene__contains=tp).order_by('-update_time')[:6]
        data = []
        for p in hot_plan:
            info = dict()
            info['name'] = p.title + '(' + p.scene + ')'
            info['create_time'] = fmt(p.create_time)
            data.append(info)
        context = {
            "status": 200,
            "msg": u'执行成功',
            "data": data
        }
        return Response(context)


class PlanContactsList(DatatableView):
    """ 预案联系人列表
    """

    render_columns = [
        ("id", "id", 0),
        ("name", "name"),
        ("phone", "phone", 0),
        ("email", "email", 0),
    ]
    model = PlanContacts

    def get_initial_queryset(self):
        """获取可查询的数据"""
        req = self.request.data
        plan_id = req.get('id')
        contacts = PlanContacts.objects.filter(plan_id=plan_id)
        return contacts


class PlanContactsOperate(APIView):
    """ 预案联系人操作
    """

    def get_objects(self, pk):
        """ 获取对象
        """
        contact = PlanContacts.objects.filter(pk=pk).first()
        return contact

    def put(self, request, pk):
        """ 修改
        """
        contact = self.get_objects(pk)
        return_instance_error(contact)
        req = request.data
        obj_serializer = c_ser(instance=contact, data=req)
        if obj_serializer.is_valid():
            obj_serializer.save()
            context = {
                "status": 200,
                "msg": u'执行成功',
            }
        else:
            msg = u'执行失败'
            for error in obj_serializer.errors:
                msg = obj_serializer.errors[error][0]
                break
            context = {
                "status": 500,
                "msg": msg,
                "error": msg
            }
        return Response(context)

    def delete(self, request, pk):
        """ 删除
        """
        contact = self.get_objects(pk)
        return_instance_error(contact)
        contact.delete()
        context = {
            "status": 200,
            "msg": u'执行成功',
        }
        return Response(context)


# class PlanContactsAdd(APIView):
#         """ 预案联系人添加
#         """
#
#         def post(self, request):
#             """ 添加联系人
#             """
#             req = request.data
#             obj_serializer = c_ser(data=req)
#             if obj_serializer.is_valid():
#                 obj = obj_serializer.save()
#                 context = {
#                     "status": 200,
#                     "msg": u'执行成功',
#                     "data": {'id': obj.id}
#                 }
#             else:
#                 msg = u'执行失败'
#                 for error in obj_serializer.errors:
#                     msg = obj_serializer.errors[error][0]
#                     break
#                 context = {
#                     "status": 500,
#                     "msg": msg,
#                     "error": msg
#                 }
#             return Response(context)

# class UploadImg(APIView):
#     """ 上传图片
#     """
#
#     def post(self, request):
#         """上传
#         """
#         img_file = request.FILES.get('img')
#         store_type = request.data.get('store_type', 0)
#         # 图片小于2M
#         if img_file.size >= 2097152:
#             context = {
#                 "status": 500,
#                 "msg": u'图片文件大于2M',
#             }
#             return Response(context)
#
#         # 生成新的文件名
#         img_ext = os.path.splitext(img_file.name)[1][1:].lower()
#         img_dir = os.path.join(settings.MEDIA_ROOT, 'op')
#         img_name = '%s.%s' % (md5(str(time.time())).hexdigest(), img_ext)
#
#         img_path = os.path.join(img_dir, img_name)
#         # 存储img 信息
#         img_store = OpImgStore.objects.create(
#             img_name=img_name, img_dir=img_dir, store_type=store_type, store_id=0)
#         # 存储到目录
#         with open(img_path, 'wb+') as f:
#             for ck in img_file.chunks():
#                 f.write(ck)
#         return_url = settings.MEDIA_URL + 'op/' + img_name
#         data = {'img_id': img_store.id, 'url': return_url}
#         context = {
#             "status": 200,
#             "msg": u'执行成功',
#             'data': data
#         }
#         return Response(context)


class LastVulSearch(APIView):
    """ 最近的漏洞搜索
        是所有用户最近的搜索
    """

    def get(self, request):
        """ 最近的预案搜索
        """
        all_search = SearchKnowledgeLog.objects.filter(search_type=0).order_by('-search_time')[:6]
        result = dict()
        for s in all_search:
            result[s.id] = {'result_id': s.result_id, 'search_time': fmt(s.search_time)}

        last_vul = VulStore.objects.filter(
            id__in=[i['result_id'] for i in result.values()])
        k_data = dict()
        for p in last_vul:
            k_data[p.id] = (p.vul_name, p.vul_id)
        data = []
        for k in result.values():
            name = k_data.get(k['result_id'])
            if not name:
                continue
            data.append({
                'id': k['result_id'],
                'name': name[0],
                'vul_id': name[1],
                'search_time': k['search_time']})

        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": data
        }
        return Response(context)


class LastHighVul(APIView):
    """ 最新高危漏洞
    """

    def get(self, request):
        """最新的高危"""
        vul_list = VulStore.objects.filter(
            vul_level__contains=u'高', data_source=1).values(
            'id', 'vul_name', 'publish_date', 'vul_id').order_by('-publish_date')[:6]
        vul_list = list(vul_list)
        for i in vul_list:
            i['level'] = 4
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": vul_list
        }
        return Response(context)


class VulDataSource(APIView):
    """ 漏洞数据来源
    """

    def get(self, request):
        """ 获取当前的数据来源"""
        data = [{'id': 1, 'data_source': u'CNNVD'},
                {'id': 2, 'data_source': u'CNVD'},
                {'id': 3, 'data_source': u'CVE'},
                ]
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": data
        }
        return Response(context)


class VulScore(APIView):
    """ 漏洞评分
    """

    def get(self, request, pk):
        """获取漏洞评分"""
        vul_obj = VulStore.objects.filter(pk=pk).first()
        if not vul_obj or not vul_obj.score:
            context = {
                "status": 500,
                "msg": u'无法获取评分',
                "error": u'找不到漏洞或漏洞无评分'
            }
            return Response(context)
        level = get_level(vul_obj)
        vul_name = vul_obj.vul_name
        score = vul_obj.score
        cvss = vul_obj.cvss
        base_data = {
            'AV': 'N',
            'AC': 'L',
            'PR': 'N',
            'UI': 'N',
            'S': 'U',
            'C': 'N',
            'I': 'N',
            'A': 'N'
        }
        for c in cvss.split('/'):
            info = c.split(':')
            for _ in base_data:
                if len(info) == 2:
                    base_data[info[0]] = info[1]
        environmental_data = {
            'MAV': 'X',
            'IR': 'X',
            'AR': 'X',
            'CR': 'X',
            'MPR': 'X',
            'MC': 'X',
            'MI': 'X',
            'MA': 'X',
            'MAC': 'X',
            'MUI': 'X',
            'MS': 'X'
        }
        result = {
            'vul_name': vul_name,
            'level': level,
            'score': score,
            'base': base_data,
            'environmental': environmental_data
        }
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": result
        }
        return Response(context)


# class VulScoreCalculation(APIView):
#     """ CVSS3.0 计算
#     """
#
#     def post(self, request):
#         """ 计算漏洞分数"""
#         req = request.data
#         firm = req.get('firm_type', 'B')
#         del req['firm_type']
#         vector_dict = req.get('base')
#         environmental = req.get('environmental')
#         vector_dict.update(environmental)
#         # 计算分数
#         vector = 'CVSS:3.0'
#         for k, v in vector_dict.items():
#             vector += '/' + k + ':' + v
#         try:
#             cs3 = cvss.CVSS3(vector)
#             score = cs3.scores()[2]
#         except Exception as e:
#             context = {
#                 "status": 500,
#                 "msg": u'向量参数错误',
#                 "data": u'向量参数错误'
#             }
#             return Response(context)
#         else:
#             firm_level = get_firm_level(firm, score)
#             context = {
#                 "status": 200,
#                 "msg": u'查询成功',
#                 "data": {'score': score, 'level': firm_level}
#             }
#             return Response(context)


# def LoadPlanPdf(request, pk):
#     """ 下载 预案库pdf 文件
#     """
#     from django.http import JsonResponse
#     obj = PlanStore.objects.filter(pk=pk).first()
#     if not obj:
#         result = {
#             "status": 500,
#             "msg": u'找不到预案',
#             "error": u'找不到预案'
#         }
#         return JsonResponse(result)
#     template_name = 'plan_pdf.html'
#     file_name = obj.title + '.pdf'
#     contacts = obj.plancontacts_set.all()
#     contacts_list = []
#     for c in contacts:
#         contacts_list.append({'name':c.name, 'phone': c.phone, 'email': c.email})
#     context = {
#         "title": obj.title,
#         "user": obj.user,
#         "level": obj.level,
#         "tag": ','.join([i.name for i in obj.tag.all()]),
#         "scene": obj.scene,
#         "brief": obj.brief,
#         "description": obj.description,
#         "contacts": contacts_list,
#         "update_time": fmt(obj.update_time),
#         "create_time": fmt(obj.create_time)
#     }
#     return html_pdf(template_name, context, file_name)


def html_to_pdf(request, pk):
    """ pdfkit 下载pdf
    """
    # 读取模板时无法加载static, 直接传路径
    static_dir = os.path.join(settings.BASE_DIR, "soc_knowledge/static")
    obj = PlanStore.objects.filter(pk=pk).first()
    template_name = 'plan_to_pdf.html'
    file_name = obj.title + '.pdf'
    contacts = obj.plancontacts_set.all()
    contacts_list = []
    for c in contacts:
        contacts_list.append({'name': c.name, 'phone': c.phone, 'email': c.email})
    context = {
        "static_dir": static_dir,
        "title": obj.title,
        "user": obj.user,
        "level": obj.level,
        "tag": ','.join([i.name for i in obj.tag.all()]),
        "scene": obj.scene,
        "brief": obj.brief,
        "description": obj.description,
        "contacts": contacts_list,
        "update_time": fmt(obj.update_time),
        "create_time": fmt(obj.create_time)
    }
    res = render_pdf(template_name, context, file_name)
    return res


class HtmlToPdf(APIView):
    """ pdfkit 下载pdf
    """

    def get(self, request, pk):
        """ 返回pdf文件路径
        """
        # 读取模板时无法加载static, 直接传路径
        static_dir = os.path.join(settings.BASE_DIR, "soc_knowledge/static")
        obj = PlanStore.objects.filter(pk=pk).first()
        template_name = 'plan_to_pdf.html'
        file_name = md5(obj.title).hexdigest() + '.pdf'
        contacts = obj.plancontacts_set.all()
        contacts_list = []
        for c in contacts:
            contacts_list.append({'name': c.name, 'phone': c.phone, 'email': c.email})
        context = {
            "static_dir": static_dir,
            "title": obj.title,
            "user": obj.user,
            "level": obj.level,
            "tag": ','.join([i.name for i in obj.tag.all()]),
            "scene": obj.scene,
            "brief": obj.brief,
            "description": obj.description,
            "contacts": contacts_list,
            "update_time": fmt(obj.update_time),
            "create_time": fmt(obj.create_time)
        }
        res = create_pdf_file(template_name, context, file_name)
        if not res:
            context = {
                "status": 500,
                "msg": u'下载失败',
                "error": u'无法下载,请检查插件'
            }
            return Response(context)
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": {"url": res}
        }
        return Response(context)


class VulVersion(APIView):
    """ 查询漏洞库版本
    """

    def get(self, request):
        """ 获取漏洞库版本库
        """
        ver = VulStoreVersion.objects.first()
        default_ver = 'v%s.01.01' % datetime.now().year
        if not ver:
            version = default_ver
        else:
            version = ver.version or default_ver
        context = {
            "status": 200,
            "msg": u'查询成功',
            "data": {"version": version}
        }
        return Response(context)


class SmList(DatatableView):
    """ SM词库列表
    """
    render_columns = [
        ("id", "id", 0),
        ("word", "word"),
    ]
    model = SmWord

    def get_initial_queryset(self):
        """获取可查询的数据"""
        sm_list = SmWord.objects.all()
        return sm_list

    def prepare_results(self, qs):
        data = []
        # 有 column 的话返回对应 column 值字典
        columns = self.get_columns()
        for item in qs:
            data_dict = {
                self.render_columns[columns.index(column)][0]: self.render_column(item, '.'.join(column.split('__')))
                for column in columns
            }
            data.append(data_dict)
        return data


class SmWordView(APIView):
    """ SM词API """
    model = SmWord

    def get(self, request, id=None):
        """
        获取词库信息
        """
        data = dict()
        # 用户id
        if id:
            data = SmWord.objects.filter(id=id).values().first()

        # 结果返回
        return Response({"status": 200, "data": data})

    def post(self, request):
        """
        创建SM词库
        """

        serializer = sm_ser(data=request.data)
        if not serializer.is_valid():
            context = {
                "status": 500,
                "msg": serializer.errors.items()[0][1][0],
                "errors": serializer.errors
            }
            return Response(context)
        else:
            word = serializer.validated_data.get('word')
            sm_word = SmWord(word=word)
            sm_word.save()
            return Response({"status": 200, 'msg': '添加成功'})

    def put(self, request):
        """
        修改SM词
        """

        serializer = sm_ser(data=request.data)
        if not serializer.is_valid():
            context = {
                "status": 500,
                "msg": serializer.errors.items()[0][1][0],
                "errors": serializer.errors
            }
            return Response(context)
        else:
            id = serializer.validated_data.get('id')
            word = serializer.validated_data.get('word')
            if id:
                # 查询该id 数据
                sm = SmWord.objects.filter(id=id)
                # 检测数据是否错误
                if not sm:
                    return Response({'msg': '数据不存在'})
                # 执行更新
                sm.update(word=word)
            # 返回给前端数据
            return Response({"status": 200, 'msg': '修改成功'})

    def delete(self, request, id):
        """
        删除SM词
        ---
        """
        try:
            sm_word = SmWord.objects.get(id=id)
        except SmWord.DoesNotExist:
            return Response({"status": 500, "msg": "白名单 Id 错误"})

        sm_word.delete()
        return Response({"status": 200, "msg": "删除成功"})


class WorkdayList(DatatableView):
    """ 工作日设置 """
    render_columns = [
        ("id", "id", 0),
        ("week", "week"),
        ("state", "state", 0),
        ("am_start_time", "am_start_time"),
        ("am_end_time", "am_end_time"),
        ("pm_start_time", "pm_start_time"),
        ("pm_end_time", "pm_end_time")
    ]
    model = WorkDay

    def get_initial_queryset(self):
        """获取可查询的数据"""
        workDay_list = WorkDay.objects.all()
        return workDay_list


class WorkdayEdit(APIView):
    """ 工作日设置 """
    model = WorkDay

    def get(self, request, id=None):
        """
        获取工作日信息
        """
        data = dict()
        # 用户id
        if id:
            data = WorkDay.objects.filter(id=id).values().first()

        # 结果返回
        return Response({"status": 200, "data": data})


class WorkdaySave(APIView):
    """ 工作日设置 """
    model = WorkDay

    def put(self, request):
        """
        修改工作日信息
        """

        serializer = WorkDaySerializer(data=request.data)
        if not serializer.is_valid():
            context = {
                "status": 500,
                "msg": serializer.errors.items()[0][1][0],
                "errors": serializer.errors
            }
            return Response(context)
        else:
            id = serializer.validated_data.get('id')
            week = serializer.validated_data.get('week')
            state = serializer.validated_data.get('state')
            am_start_time = serializer.validated_data.get('am_start_time')
            am_end_time = serializer.validated_data.get('am_end_time')
            pm_start_time = serializer.validated_data.get('pm_start_time')
            pm_end_time = serializer.validated_data.get('pm_end_time')
            if id:
                # 查询该id 数据
                workDay = WorkDay.objects.filter(id=id)
                # 检测数据是否错误
                if not workDay:
                    return Response({'msg': '数据不存在'})
                # 执行更新
                workDay.update(week=week, state=state, am_start_time=am_start_time, am_end_time=am_end_time,
                               pm_start_time=pm_start_time, pm_end_time=pm_end_time)
            # 返回给前端数据
            return Response({"status": 200, 'msg': '保存成功'})


class GroupRuleList(APIView):
    """
    安全规则组
    """

    def post(self, request):
        """
        安全规则组
        """
        group_rule_list = GroupRule.objects.all().values().order_by('id')
        result = []
        for item in group_rule_list:
            result.append({
                'id': item['id'],
                'group_name': item['group_name']
            })
        return Response({"status": 200, "msg": "查询成功", "data": result})


class GroupRuleView(APIView):
    """
    安全规则组
    """
    model = GroupRule

    def get(self, request, id=None):
        """
        获取安全规则组信息
        """
        data = {}
        # 用户id
        if id:
            data = GroupRule.objects.filter(id=id).values().first()

        # 结果返回
        return Response({"status": 200, "data": data})

    def post(self, request):
        """
        创建安全规则
        """

        obj_serializer = group_rule_ser(data=request.data, context={'request': request})
        if obj_serializer.is_valid():
            instance = obj_serializer.save()
            return Response({"status": 200, "msg": "添加成功", "data": obj_serializer.data})
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})

    def put(self, request, id):
        """
        修改安全规则
        """

        try:
            instance = GroupRule.objects.get(id=id)
        except GroupRule.DoesNotExist:
            context = {
                "status": 500,
                "error": u"安全规则组不存在",
                "msg": u"安全规则组不存在"
            }
            return Response(context)
        if not instance:
            return Response({"status": 500, "msg": "获取对象错误"})
        obj_serializer = group_rule_ser(
            instance=instance,
            data=request.data,
            context={'request': request},
            partial=True)

        if obj_serializer.is_valid():
            instance = obj_serializer.save()
            return Response({"status": 200, "msg": "修改成功", "data": obj_serializer.data})
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})

    def delete(self, request, id):
        """
        安全规则
        """
        try:
            group_rule = GroupRule.objects.get(id=id)
        except GroupRule.DoesNotExist:
            return Response({"status": 500, "msg": "安全规则组删除错误"})

        group_rule.delete()
        return Response({"status": 200, "msg": "删除成功"})


class AlarmRuleList(DatatableView):
    """
    安全规则
    """
    render_columns = [
        ("id", "id", 0),
        ("rule_name", "rule_name"),
        ("description", "description"),
        ("level", "level"),
        ("status", "status"),
        ("content", "content"),
        ("time_type", "time_type"),
        ("interval", "interval"),
        ("time_start", "time_start"),
        ("time_end", "time_end"),
        ("update_time", "update_time"),
        ("create_time", "create_time"),

    ]
    model = AlarmRule

    def get_initial_queryset(self):
        """获取可查询的数据"""
        group_id = self.request.data.get('group_id')
        search = self.request.data.get('search[value]')
        rule_list = AlarmRule.objects.all()
        if group_id:
            rule_list = rule_list.filter(group_id=group_id)
        if search:
            rule_list = rule_list.filter(rule_name__icontains=search)
        return rule_list.order_by('-create_time')

    def filter_queryset(self, qs):
        return qs

    def prepare_results(self, qs):
        data = []
        # 有 column 的话返回对应 column 值字典
        columns = self.get_columns()
        for item in qs:
            data_dict = {
                self.render_columns[columns.index(column)][0]: self.render_column(item, '.'.join(column.split('__')))
                for column in columns
            }
            data_dict['create_time'] = datetime.strftime(item.create_time, '%Y-%m-%d %H:%M:%S')
            data.append(data_dict)
        return data


class AlarmRuleView(APIView):
    """
    安全规则
    """
    model = AlarmRule

    def get(self, request, id=None):
        """
        获取安全规则信息
        """
        data = {}
        # 用户id
        if id:
            data = AlarmRule.objects.filter(id=id).values().first()

        # 结果返回
        return Response({"status": 200, "data": data})

    def post(self, request):
        """
        创建安全规则
        """

        obj_serializer = alarm_rule_ser(data=request.data, context={'request': request})
        if obj_serializer.is_valid():
            instance = obj_serializer.save()
            return Response({"status": 200, "msg": "添加成功", "data": obj_serializer.data})
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})

    def put(self, request):
        """
        修改安全规则
        """
        instance = dict()
        try:
            id = request.data.get('id')
            if id:
                instance = AlarmRule.objects.get(id=id)
        except AlarmRule.DoesNotExist:
            context = {
                "status": 500,
                "error": u"安全规则不存在",
                "msg": u"安全规则不存在"
            }
            return Response(context)
        if not instance:
            return Response({"status": 500, "msg": "获取对象错误"})
        obj_serializer = alarm_rule_ser(
            instance=instance,
            data=request.data,
            context={'request': request},
            partial=True)

        if obj_serializer.is_valid():
            instance = obj_serializer.save()
            return Response({"status": 200, "msg": "修改成功", "data": obj_serializer.data})
        else:
            errors = obj_serializer.errors
            return Response({"status": 500, "msg": errors.items()[0][1][0], "error": errors})

    def delete(self, request):
        """
        安全规则
        """
        try:
            ids = request.data.get('ids')
            if ids:
                AlarmRule.objects.filter(id__in=ids.split(',')).delete()
        except Exception as e:
            return Response({"status": 500, "msg": "安全规则删除错误"})

        return Response({"status": 200, "msg": "删除成功"})


class AlarmRuleStartView(APIView):
    """
    告警规则开启
    """

    def post(self, request):
        """
        告警规则开启
        """
        try:
            ids = request.data.get('ids')
            if ids:
                AlarmRule.objects.filter(id__in=ids.split(',')).update(status=1)
        except Exception as e:
            return Response({"status": 500, "msg": "安全规则开启失败"})

        return Response({"status": 200, "msg": "安全规则开启成功"})


class AlarmRuleStopView(APIView):
    """
    告警规则关闭
    """

    def post(self, request):
        """
        告警规则关闭
        """
        try:
            ids = request.data.get('ids')
            if ids:
                AlarmRule.objects.filter(id__in=ids.split(',')).update(status=-1)
        except Exception as e:
            return Response({"status": 500, "msg": "安全规则关闭失败"})

        return Response({"status": 200, "msg": "安全规则关闭成功"})


class AlarmRuleRunView(APIView):
    """
    立即执行安全规则
    """

    def post(self, request):
        """
        事件类型
        """
        try:
            id = request.data.get('id')
            if id:
                day = datetime.strftime(datetime.now(), "%Y-%m-%d")
                alarm_rule = AlarmRule.objects.get(id=id)
                logging.info('执行规则{}'.format(alarm_rule.rule_name))
                sql_list = alarm_rule.sql
                for sql_str in sql_list.split('@'):
                    sqls = sql_str.split('|')
                    sql = sqls[0]
                    count = 0
                    if len(sqls) == 2:
                        count = int(sqls[1])
                    data_list = []
                    # 防火墙规则
                    if id in ('1', '2', '3'):
                        ip_sql = sql.replace('$', day.replace('-', '')).replace('all-event-*',
                                                                                'all-event-{}-*'.format(day))
                        ip_sql = ip_sql.replace(' * ',
                                                ' src_ip,count(*) count_ ') + ' and event_source = 1 group by src_ip'
                        result = es_select.exec_es_sql(sql=ip_sql)
                        ip_list = []
                        for count_ in result:
                            if count_['count_'] >= count:
                                ip_list = ['\'{}\''.format(count_['src_ip'])]
                        if ip_list:
                            sql = sql.replace('$', day.replace('-', '')).replace('all-event-*',
                                                                                 'all-event-{}-*'.format(day))
                            sql = sql + ' and event_source = 1 and src_ip in ({})'.format(','.join(ip_list))
                            logging.info('执行规则sql:{}'.format(sql))
                            data_list = es_select.exec_es_sql(sql=sql)
                            self.add_alarm_log(alarm_rule=alarm_rule, data_list=data_list)
                    else:
                        sql = sql.replace('$', day.replace('-', '')).replace('all-event-*',
                                                                             'all-event-{}-*'.format(day))
                        logging.info('执行规则sql:{}'.format(sql))
                        data_list = es_select.exec_es_sql(sql=sql)
                        if (count == 0) or (count > 0 and len(data_list) >= count):
                            self.add_alarm_log(alarm_rule=alarm_rule, data_list=data_list)

        except Exception as e:
            logging.error(e)
            return Response({"status": 500, "msg": "执行失败"})

        return Response({"status": 200, "msg": "执行成功"})

    def add_alarm_log(self, alarm_rule, data_list):
        '''
        批量添加告警数据
        '''
        logs = []
        for item in data_list:
            alarm_log = AlarmLog()
            alarm_log.rule = alarm_rule
            alarm_log.group_name = alarm_rule.group.group_name
            alarm_log.rule_name = alarm_rule.rule_name
            alarm_log.src_ip = item['src_ip']
            alarm_log.src_port = item['src_port']
            alarm_log.dst_ip = item['dst_ip']
            alarm_log.dst_port = item['dst_port']
            alarm_log.tran_protocol = item['tran_protocol']
            alarm_log.app_protocol = item['app_protocol']
            alarm_log.event_host = item['event_host']
            alarm_log.event_time = datetime.now()
            alarm_log.alarm_time = datetime.now()
            alarm_log.alarm_level = alarm_rule.level
            uuids = item['uuids'] if 'uuids' in item else []
            alarm_log.old_log_list = [uuid.encode("utf-8") for uuid in uuids]
            alarm_log.event_source = item['event_source']
            logs.append(alarm_log)

            if len(logs) > 100:
                AlarmLog.objects.bulk_create(logs)
                logs = []
        if logs:
            AlarmLog.objects.bulk_create(logs)


class AlarmRuleEventTypeView(APIView):
    """
    事件类型
    """

    def post(self, request):
        """
        事件类型
        """
        sql = 'SELECT event_three_type,count(*) count_ FROM all-event-* group by event_three_type'
        result = es_select.exec_es_sql(sql=sql)
        data = []
        for item in result:
            data.append({
                'id': item['event_three_type'],
                'name': item['event_three_type'],
            })
        return Response({"status": 200, "data": data})


class AlarmTypeView(APIView):
    """
    告警类型
    """

    def post(self, request):
        """
        告警类型
        """
        sql = 'select t.group_name,count(*) count_,count(DISTINCT src_ip) src_count ' \
              'from alarm_log t GROUP BY t.group_name order by count_ desc'
        result = mysql_select.exec_sql(sql=sql)
        return Response({"status": 200, "data": result})


class AlarmMonitorView(APIView):
    """
    告警监测
    """

    def post(self, request):
        """
        告警监测
        """
        group_name = request.data.get('group_name')
        result = []
        if group_name:
            sql = 'select t.rule_name,count(*) count_ from alarm_log t ' \
                  'where t.group_name=\'{}\' GROUP BY t.rule_name order by count_ desc '.format(group_name)
            result = mysql_select.exec_sql(sql=sql)
        return Response({"status": 200, "data": result})


class AlarmSourceView(APIView):
    """
    告警源
    """

    def post(self, request):
        """
        告警源
        """
        group_name = request.data.get('group_name')
        rule_name = request.data.get('rule_name')
        result = []
        if group_name and rule_name:
            sql = 'select t.src_ip,count(*) count_ from alarm_log t ' \
                  'where t.group_name=\'{}\' and t.rule_name=\'{}\' ' \
                  'GROUP BY t.src_ip order by count_ desc'.format(group_name, rule_name)
            result = mysql_select.exec_sql(sql=sql)
        return Response({"status": 200, "data": result})


class AlarmTrendView(APIView):
    """
    告警趋势
    """

    def post(self, request):
        """
        告警趋势
        """
        group_name = request.data.get('group_name')
        rule_name = request.data.get('rule_name')
        src_ip = request.data.get('src_ip')
        where = ''
        if group_name:
            where += 'AND group_name=\'{}\' '.format(group_name)
        if rule_name:
            where += 'AND rule_name=\'{}\' '.format(rule_name)
        if src_ip:
            where += 'AND src_ip=\'{}\' '.format(src_ip)
        sql = 'select DATE_FORMAT(alarm_time,\'%Y-%m-%d\') days,count(*) count_ ' \
              'from alarm_log where 1=1 {} group by days order by alarm_time desc limit 30'.format(where)
        result = mysql_select.exec_sql(sql=sql)
        result = sorted(result, key=lambda i: i['days'])
        return Response({"status": 200, "data": result})


class AlarmListView(DatatableView):
    """
    告警列表
    """
    render_columns = [
        ("id", "id", 0),
        ("group_name", "group_name"),
        ("rule_name", "rule_name"),
        ("src_ip", "src_ip"),
        ("src_port", "src_port"),
        ("tran_protocol", "tran_protocol"),
        ("app_protocol", "app_protocol"),
        ("dst_ip", "dst_ip"),
        ("dst_port", "dst_port"),
        ("event_host", "event_host"),
        ("event_time", "event_time"),
        ("alarm_time", "alarm_time"),
        ("alarm_level", "alarm_level"),
        ("event_source", "event_source"),
        ("status", "status")

    ]
    model = AlarmLog

    def get_initial_queryset(self):
        """获取可查询的数据"""
        group_name = self.request.data.get('group_name')
        rule_name = self.request.data.get('rule_name')
        src_ip = self.request.data.get('src_ip')
        alarm_level = self.request.data.get('alarm_level')
        search = self.request.data.get('search[value]')
        alarm_log = AlarmLog.objects.all()
        if group_name:
            alarm_log = alarm_log.filter(group_name=group_name)
        if rule_name:
            alarm_log = alarm_log.filter(rule_name=rule_name)
        if src_ip:
            alarm_log = alarm_log.filter(src_ip=src_ip)
        if alarm_level:
            alarm_log = alarm_log.filter(alarm_level=alarm_level)
        if search:
            alarm_log = alarm_log.filter(Q(src_ip__contains=search)
                                         | Q(src_port__contains=search)
                                         | Q(dst_ip__contains=search)
                                         | Q(dst_port__contains=search)
                                         | Q(event_host__contains=search)
                                         | Q(group_name__icontains=search))
        return alarm_log.order_by('-alarm_time')

    def filter_queryset(self, qs):
        return qs

    def prepare_results(self, qs):
        data = []
        # 有 column 的话返回对应 column 值字典
        columns = self.get_columns()
        for item in qs:
            data_dict = {
                self.render_columns[columns.index(column)][0]: self.render_column(item, '.'.join(column.split('__')))
                for column in columns
            }
            data_dict['alarm_time'] = datetime.strftime(item.alarm_time, '%Y-%m-%d %H:%M:%S')
            data.append(data_dict)
        return data


class AlarmLogStopView(APIView):
    """
    关闭告警日志
    """

    def post(self, request):
        """
        关闭告警日志
        """
        try:
            ids = request.data.get('ids')
            if ids:
                AlarmLog.objects.filter(id__in=ids.split(',')).update(status=0)
        except Exception as e:
            return Response({"status": 500, "msg": "告警日志关闭失败"})

        return Response({"status": 200, "msg": "告警日志关闭成功"})


class AlarmLogView(APIView):
    """
    告警日志列表
    """

    def post(self, request):
        """
        告警日志列表
        """

        id = self.request.data.get('id')
        start = self.request.data.get("start", 0)
        length = self.request.data.get("length", 10)
        result = []
        count = 0
        if id:
            alarm_log = AlarmLog.objects.filter(id=id).values()
            if alarm_log:
                event_source = alarm_log.first()['event_source']
                old_log_list = alarm_log.first()['old_log_list']
                event_source_type = ['1', '2', '3', '4', '5', '6', '7']
                event_source_index = ['ssa-ag-fw-*', 'ssa-ag-ids-*', 'ssa-ag-database-*', 'ssa-ag-bd-*', 'ssa-ag-gl-*',
                                      'ssa-ag-360-*', 'ssa-ag-all-terminal-*']
                index = event_source_index[event_source_type.index(event_source)]
                if old_log_list:
                    old_log_list = old_log_list.replace("[", "").replace("]", "")
                    count_sql = 'SELECT count(*) count_ FROM {} where uuid in ({})'.format(index, old_log_list)
                    count_result = es_select.exec_es_sql(sql=count_sql)
                    if count_result:
                        count = count_result[0]['count_']
                    sql = 'SELECT * FROM {} where uuid in ({})'.format(index, old_log_list)
                    data_list = es_select.exec_es_sql(sql=sql)
                    for item in data_list:
                        result.append({
                            'stastic_time': item['@timestamp'].replace('T', ' ').replace('Z', ''),
                            'event_host': item['src_ip'],
                            'event_detail': json.dumps(item).decode('unicode_escape')
                        })

        context = {
            'draw': 0,
            'recordsTotal': count,
            'recordsFiltered': count,
            'data': result,
            'result': 'ok'
        }
        return Response(context)
