# coding: utf-8
"""
select2 filter
"""
import math


def select2_filter(request, data_list, all=1, page_default=1, page_size_default=5):
    """过滤"""
    # q = request.DATA.get("q", '')
    page = request.DATA.get("page", page_default)
    all = request.DATA.get("all", all)
    if not page:
        page = 1
    page = int(page)
    page_size = request.DATA.get("page_size", page_size_default)  # 每页显式的数目
    if not page_size:
        page_size = 5  # 默认一页显示5个数据
    page_size = int(page_size)
    start = (page - 1) * page_size
    end = page * page_size
    # data_list = ModelNetdeviceType.objects.filter(name__contains=q).values("id", "name")
    total_count = len(data_list)
    if all == 1:
        page = 1
        # page_size = total_count
        page_size = page_size if total_count == 0 else total_count
        start = 0
        end = total_count
    total_page = math.ceil(float(total_count) / page_size)
    if page < 0 or page > total_page:
        incomplete_results = False
    elif page == total_page:
        incomplete_results = False
    else:
        incomplete_results = True
    try:  # 处理越界操作
        response_list = data_list[start:end]
    except Exception as e:
        response_list = []
        incomplete_results = False
    context = {
        "total_count": total_count,
        "incomplete_results": incomplete_results,
        "items": response_list
    }
    return context
