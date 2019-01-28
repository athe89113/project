# coding=utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from utils import monitor


class MonitorView(APIView):
    """监控项"""
    items = {
       "cpu": monitor.CpuMonitor,
       "net": monitor.NetMonitor,
       "disk": monitor.DiskMonitor,
       "mem": monitor.MenMonitor,
    }

    def get(self, request):
        """获取监控项数据"""
        item = request.GET.get("item")
        tool_class = self.items.get(item)
        if not tool_class:
            return Response({"status": 500, "msg": "监控项错误"})
        tool = tool_class()
        data = tool.get_line_chart()
        return Response({"status": 200, "data": data})


class MonitorViewAll(APIView):
    """监控项"""
    items = {
       "cpu": monitor.CpuMonitor,
       "net": monitor.NetMonitor,
       "disk": monitor.DiskMonitor,
       "mem": monitor.MenMonitor,
    }

    def get(self, request):
        """获取所有监控项数据"""
        result = dict()
        for item, tool_class in self.items.items():
            tool = tool_class()
            data = tool.get_line_chart()
            result[item] = data
        return Response({"status": 200, "data": result})
