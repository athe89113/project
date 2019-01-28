# coding=utf-8
from __future__ import unicode_literals

from base_data import BaseData

class AssetTotalData(BaseData):
    """
    资产总数
    """

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "资产总数", "data": [19, 33, 88, 22, 66, 44, 11]}
            ]
        }

    def data(self):
        from soc import models
        # 取上架的数据
        qs = models.LifeCycle.objects.filter(event=3)
        labels, data = self.query_orm_cycle(qs, "time", is_range=False)
        data = {
            "labels": labels,
            "data": [
                {"name": "资产总数", "data": data}
            ]
        }
        return data

class AssetAddTotalData(BaseData):
    """
    新增资产总数
    """
    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "新增资产总数", "data": [19, 33, 88, 22, 66, 44, 11]}
            ]
        }

    def data(self):
        # 取上架的数据
        from soc import models
        qs = models.LifeCycle.objects.filter(event=3)
        labels, data = self.query_orm_cycle(qs, "time", is_range=True)
        data = {
            "labels": labels,
            "data": [
                {"name": "新增资产总数", "data": data}
            ]
        }
        return data

class AssetTypeData(BaseData):
    """
    资产类型
    """

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "服务器", "data": [19, 33, 88, 22, 66, 44, 11]},
                {"name": "网络设备", "data": [4, 22, 55, 99, 77, 22, 77]}
            ]
        }

    def data(self):
        # 取上架的数据
        from soc import models
        qs = models.LifeCycle.objects.filter(event=3)
        server_qs = qs.filter(asset__server__isnull=False)
        net_device_qs = qs.filter(asset__netdevice__isnull=False)

        labels, server_data = self.query_orm_cycle(server_qs, "time", is_range=False)
        labels, net_device = self.query_orm_cycle(net_device_qs, "time", is_range=False)
        data = {
            "labels": labels,
            "data": [
                {"name": "服务器", "data": server_data},
                {"name": "网络设备", "data": net_device},
                # {"name": "", "data": server_data},
            ]
        }
        return data

class SecurityAttackData(BaseData):
    """
    攻击事件数统计
    """
    ES_KEY = "security-total_count"
    SUM_KYE = "data.security_total_count"

    DISPALY_MAP = {
        "data.security_total_count": "攻击事件次数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "攻击事件数", "data": [19, 33, 88, 22, 66, 44, 11]},
            ]
        }


    def data(self):
        return self.fetch_es_sum_data()


class SecurityAttackSrcIpData(BaseData):
    """
    攻击来源IP统计
    """
    ES_KEY = "security-source_count"
    # SUM_KYE = "data.network_in_bytes"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.security_src_ip"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.security_src_ip": "攻击来源IP",
        "data.count": "次数",
    }


    @classmethod
    def demo_data(cls):
        data = {
            u'labels': [u'45.45.45.45', u'50.67.45.45', u'50.67.45.45', u'34.88.88.123', u'138.23.45.42'],
            u'data': [
                {u'data': [1188, 1176, 1173, 1165, 1163], u'name': cls.DISPALY_MAP[cls.VALUE_KYE]}
            ]
        }
        return data

    def data(self):
        """
        获取ES数据
        """
        return self.fetch_es_top_data()

class SecurityAttackDstIpData(BaseData):
    """
    攻击目的IP统计
    """
    ES_KEY = "security-dst_ip_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.security_dst_ip"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.security_dst_ip": "攻击目标IP",
        "data.count": "次数",
    }

    @classmethod
    def demo_data(cls):
        data = {
            u'labels': [u'45.45.45.45', u'50.67.45.45', u'50.67.45.45', u'34.88.88.123', u'138.23.45.42'],
            u'data': [
                {u'data': [1188, 1176, 1173, 1165, 1163], u'name': cls.DISPALY_MAP[cls.VALUE_KYE]}
            ]
        }
        return data

    def data(self):
        """
        获取ES数据
        """
        return self.fetch_es_top_data()



class SecurityAttackLevelData(BaseData):
    """
    攻击严重等级统计
    """
    ES_KEY = "security-level_count"
    TYPE_LIST = ['严重', '高', '中', '低', 'info']
    TYPE_FIELD = "data.security_level"
    VALUE_KYE = TYPE_FIELD
    SUM_KYE = "data.count"

    DISPALY_MAP = {
        # "data.security_src_ip_location": "攻击来源地址",
        "data.security_level": "攻击严重等级",
        "data.count": "次数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['严重', '高', '中', '低', 'info'],
            "data": [
                {"name": "攻击事件数", "data": [12, 33, 88, 22, 66]},
            ]
        }

    def data(self):
        """
        获取ES数据
        """
        return self.fetch_es_types_data()

class SecurityAttackTypeData(BaseData):
    """
    攻击类型占比统计
    """

    ES_KEY = "security-total_count"

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "WAF", "data": [19, 33, 88, 22, 66, 44, 11]},
                {"name": "IDS", "data": [4, 22, 55, 99, 77, 22, 77]},
                {"name": "数据库审计", "data": [12, 1, 88, 33, 99, 221, 88]},
                {"name": "防火墙", "data": [125, 88, 33, 1, 219, 22, 88]},
            ]
        }

    def data(self):
        data = [
            {"name": "WAF", "data": []},
            {"name": "IDS", "data": []},
            {"name": "数据库审计", "data": []},
            {"name": "防火墙", "data": []},
        ]
        labels = []
        for gte_time, lte_time in self.generate_time_range():
            labels.append(gte_time)
            data[0]["data"].append(self._fetch_es_sum_data(gte_time, lte_time, sum_key="data.security_waf_count"))
            data[1]["data"].append(self._fetch_es_sum_data(gte_time, lte_time, sum_key="data.security_ids_count"))
            data[2]["data"].append(self._fetch_es_sum_data(gte_time, lte_time, sum_key="data.security_db_audit_count"))
            data[3]["data"].append(self._fetch_es_sum_data(gte_time, lte_time, sum_key="data.security_firewall_count"))
        # labels = self
        labels = self.time_format_cycle(labels)
        # print(json.dumps({"labels": labels, "data": data}))
        return {"labels": labels, "data": data}


class SecurityThroughputData(BaseData):
    """
    异常流量统计
    """

    ES_KEY = "network-throughput"

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "异常入口流量", "data": [19, 33, 88, 22, 66, 44, 11]},
                {"name": "异常出口流量", "data": [4, 22, 55, 99, 77, 22, 77]},
            ]
        }

    def data(self):
        data = [
            {"name": "异常入口流量", "data": []},
            {"name": "异常出口流量", "data": []},
        ]
        labels = []
        for gte_time, lte_time in self.generate_time_range():
            labels.append(gte_time)
            data[0]["data"].append(self._fetch_es_sum_data(gte_time, lte_time, sum_key="data.network_in_bytes"))
            data[1]["data"].append(self._fetch_es_sum_data(gte_time, lte_time, sum_key="data.network_out_bytes"))
        labels = self.time_format_cycle(labels)
        return {"labels": labels, "data": data}

class SecurityThroughputPeakData(BaseData):
    """
    异常流量峰值统计
    """

    ES_KEY = "network-abnormal_throughput_peak"

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "异常入口流量峰值", "data": [19, 33, 88, 22, 66, 44, 11]},
                {"name": "异常出口流量峰值", "data": [4, 22, 55, 99, 77, 22, 77]},
            ]
        }

    def data(self):
        data = [
            {"name": "异常入口流量峰值", "data": []},
            {"name": "异常出口流量峰值", "data": []},
        ]
        labels = []
        for gte_time, lte_time in self.generate_time_range():
            labels.append(gte_time)
            data[0]["data"].append(self._fetch_es_max_data(gte_time, lte_time, max_key="data.network_max_in_bytes"))
            data[1]["data"].append(self._fetch_es_max_data(gte_time, lte_time, max_key="data.network_max_out_bytes"))
        labels = self.time_format_cycle(labels)
        return {"labels": labels, "data": data}

class SecurityAttackSrcIpLocationData(SecurityAttackSrcIpData):
    """
    攻击来源IP位置统计
    """
    ES_KEY = "security-source_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.security_src_ip_location"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.security_src_ip_location": "攻击来源IP位置",
        "data.count": "次数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['11.11.11.1', '11.11.11.2', '11.11.11.3', '11.11.11.4', '11.11.11.5'],
            "data": [
                {"name": "", "data": [19, 33, 88, 22, 66]},
            ]
        }

class SecurityAttackDtsIpLocationData(SecurityAttackSrcIpData):
    """
    攻击目标IP位置统计
    """
    ES_KEY = "security-dst_ip_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.security_dts_ip_location"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.security_dts_ip_location": "攻击目标IP位置",
        "data.count": "次数",
    }

class VirusTotalCountData(BaseData):
    """
    僵木蠕感染数统计
    """

    ES_KEY = "virus-total_count"
    SUM_KYE = "data.count"

    DISPALY_MAP = {
        "data.count": "僵木蠕总数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "僵木蠕总数", "data": [19, 33, 88, 22, 66, 44, 11]},
            ]
        }

    def data(self):
        return self.fetch_es_sum_data()

class VirusBtwTopData(BaseData):
    """
    严重僵木蠕感染数统计
    """

    ES_KEY = "virus-btw_asset_top"
    ORDER_KYE = "data.virus_total_count"
    VALUE_KYE = "data.virus_virusname"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.virus_virusname": "病毒名称",
        "data.virus_total_count": "次数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "严重僵木蠕感染数统计", "data": [19, 33, 88, 22, 66, 44, 11]},
            ]
        }


    def data(self):
        return self.fetch_es_top_data()

class VirusBtwAssetCountData(BaseData):
    """
    僵木蠕感染资产数统计
    """
    ES_KEY = "virus-asset_top"
    SUM_KYE = "data.virus_total_count"

    DISPALY_MAP = {
        "data.virus_total_count": "僵木蠕总数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "僵木蠕感染资产数统计", "data": [19, 33, 88, 22, 66, 44, 11]},
            ]
        }

    def data(self):
        return self.fetch_es_sum_data()

class VirusBtwAssetTopData(BaseData):
    """
    僵木蠕感染资产IP TOP
    """

    ES_KEY = "virus-asset_top"
    ORDER_KYE = "data.virus_total_count"
    VALUE_KYE = "data.virus_host_ip"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.virus_host_ip": "资产IP出现次数",
        "data.virus_total_count": "次数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07'],
            "data": [
                {"name": "僵木蠕感染资产", "data": [19, 33, 88, 22, 66, 44, 11]},
            ]
        }

    def data(self):
        return self.fetch_es_top_data()



class VulTotalCountData(BaseData):
    """
    漏洞总数统计
    """

    ES_KEY = "vul-vul_total_count"
    SUM_KYE = "data.vul_total_count"

    DISPALY_MAP = {
        "data.vul_total_count": "漏洞总数",
    }

    def data(self):
        return self.fetch_es_sum_data()


class VulTotalTopData(BaseData):
    """
    严重漏洞占比统计
    """

    ES_KEY = "vul-vul_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.vul_vuln_name"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.vul_vuln_name": "漏洞出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class VulAssetTopData(BaseData):
    """
    漏洞资产数统计
    """

    ES_KEY = "vul-vul_ip_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.vul_ip"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.vul_ip": "漏洞资产IP次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class VulTypeTopData(BaseData):
    """
    漏洞威胁类型
    """

    ES_KEY = "vul-vul_threat_type_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.vul_threat_type"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.vul_threat_type": "漏洞威胁类型出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class VulNewTopData(BaseData):
    """
    风险URL TOP
    """

    ES_KEY = "vul-vul_risk_url_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.vul_risk_url"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.vul_risk_url": "URL出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()


class WeekPasswordCountData(BaseData):
    """
    弱口令总数统计
    """

    ES_KEY = "weak-password-host_count"
    SUM_KYE = "data.count"

    DISPALY_MAP = {
        "data.count": "漏洞总数",
    }

    def data(self):
        return self.fetch_es_sum_data()

class WeekPasswordTopProtocolData(BaseData):
    """
    week_password_top_protocol_data
    
    弱口令协议TOP统计
    """

    ES_KEY = "weak-password-host_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.weak_password_protocol"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.weak_password_protocol": "协议出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class WebLogLocaltionData(BaseData):
    """
    访问源地区统计
    """

    ES_KEY = "web-log-ip_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.web_log_location"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.web_log_location": "地区出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class WebLogIpData(BaseData):
    """
    访问源IP统计
    """

    ES_KEY = "web-log-ip_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.web_log_ip"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.web_log_ip": "IP出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class WebLogPvData(BaseData):
    """
    PV统计
    """

    ES_KEY = "web-log-pv"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.web_log_url"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.web_log_url": "PV",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class WebLogUvData(BaseData):
    """
    PV统计
    """

    ES_KEY = "web-log-uv"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.web_log_ip"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.web_log_ip": "UV",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class WebLogBrowserData(BaseData):
    """
    浏览器类型
    """

    ES_KEY = "web-log-browser_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.web_log_browser"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.web_log_browser": "浏览器出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class WebLogOsData(BaseData):
    """
    OS类型
    """

    ES_KEY = "web-log-os_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.web_log_os"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.web_log_os": "操作系统出现次数",
        "data.count": "次数",
    }

    def data(self):
        return self.fetch_es_top_data()

class WebLogStatusData(BaseData):
    """
    OS类型
    """

    ES_KEY = "web-log-http_status_count"
    ORDER_KYE = "data.count"
    VALUE_KYE = "data.web_log_status"
    TOP_COUNT = 5

    DISPALY_MAP = {
        "data.web_log_status": "响应码出现次数",
        "data.count": "次数",
    }

    @classmethod
    def demo_data(cls):
        return {
            "labels": ["2xx", '3xx', '4xx', '5xx'],
            "data": [
                {"name": "01-01", "data": [9991, 291, 3121, 665]},
                {"name": "01-02", "data": [8111, 3991, 1233, 1665]},
                {"name": "01-03", "data": [10102, 812, 2131, 365]},
            ]
        }

    def data(self):
        return self.fetch_es_top_data()


if __name__ == "__main__":
    pass