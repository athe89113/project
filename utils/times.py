# coding: utf-8
from django.utils import timezone


def get_next_scan_time_ssa(start_date, time_s, period_type, days=1):
    """
    获取下次执行的时间 for 数据采集
    period_type: 1 自定义,2 每小时, 3 每天, 4 每周, 5 每月 6 执行一次
    自定义
        从 start_date + time_s 开始 每隔 days 小时 运行一次
    每小时
        每个小时的time_s(取分)运行一次
    start_date 日期格式
    time_s 时间格式
    """
    now = timezone.localtime(timezone.now())
    time_now = timezone.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    # 秒？
    hour = time_s.hour
    minute = time_s.minute
    year = start_date.year
    month = start_date.month
    day = start_date.day
    dayth = start_date.isoweekday()  # 周日为0开始算
    start_time = timezone.datetime(year, month, day, hour, minute)
    if period_type == 1:
        # 自定义 从开始时间起 每隔days小时执行一次
        if start_time > time_now:
            # 未来时间 也就是自定义时间的第一次时间
            return start_time
        else:
            while start_time <= time_now:
                start_time = start_time + timezone.timedelta(hours=days)
            return start_time
    elif period_type == 2:
        # 每小时
        while start_time <= time_now:
            start_time = start_time + timezone.timedelta(hours=1)
        return start_time
    elif period_type == 3:
        # 每天
        while start_time <= time_now:
            start_time = start_time + timezone.timedelta(days=days)
        return start_time
    elif period_type == 4:
        # 每周
        if dayth > days:
            delta = 7 - (dayth - days)
        else:
            delta = days - dayth
        return start_time + timezone.timedelta(days=delta)
    elif period_type == 5:
        # 每月
        # 如果当月没有31号之类 自动算下一个月
        while True:
            if day > days:
                day = days
                month += 1
                if month == 13:
                    month = 1
                    year += 1
            else:
                day = days
            try:
                mytime = timezone.datetime(year, month, day, hour, minute)
                break
            except ValueError:
                month += 1
                if month == 13:
                    month = 1
                    year += 1
                pass
        return mytime
    elif period_type == 6:
        # 指定时间只执行一次
        return start_time

if __name__ == "__main__":

    def test():
        from django.utils import timezone
        print("自定义时间测试")
        start_date = timezone.datetime(2018, 1, 1, 1, 1).date()
        time_s = timezone.datetime(2018, 1, 1, 1, 1).time()
        print(get_next_scan_time_ssa(start_date, time_s, 1, days=24),)
        print("每小时时间测试测试")
        # start_date = timezone.datetime(2018, 3, 1, 1, 1).date()
        time_s = timezone.datetime(2018, 3, 1, 1, 1).time()
        print(get_next_scan_time_ssa(timezone.now(), time_s, 2),)
    test()
