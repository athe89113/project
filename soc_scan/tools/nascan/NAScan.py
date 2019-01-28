# -*- coding:utf-8 -*-
import thread

from soc_scan.tools.nascan.nalib.common import *
from soc_scan.tools.nascan.nalib.start import *

logger = logging.getLogger('soc_scan')


def na_start():
    '''
    NAscan
    '''
    try:
        CONFIG_INI = get_config()  # 读取配置
        logger.info(u'获取配置成功')
        STATISTICS = get_statistics()  # 读取统计信息
        MASSCAN_AC = [0]
        NACHANGE = [0]
        thread.start_new_thread(monitor, (CONFIG_INI, STATISTICS, NACHANGE))  # 心跳线程
        thread.start_new_thread(cruise, (STATISTICS, MASSCAN_AC))  # 失效记录删除线程
        socket.setdefaulttimeout(int(CONFIG_INI['Timeout']) / 2)  # 设置连接超时
        ac_data = []
        while True:
            now_time = time.localtime()
            now_hour = now_time.tm_hour
            now_day = now_time.tm_mday
            now_date = str(now_time.tm_year) + str(now_time.tm_mon) + str(now_day)
            cy_day, ac_hour = CONFIG_INI['Cycle'].split('|')
            logger.info(u'扫描规则: ' + str(CONFIG_INI['Cycle']))
            if (now_hour == int(ac_hour) and now_day % int(cy_day) == 0 and now_date not in ac_data) or NACHANGE[
                0]:  # 判断是否进入扫描时段
                ac_data.append(now_date)
                NACHANGE[0] = 0
                logger.info(u'开始扫描')
                s = start(CONFIG_INI)
                s.masscan_ac = MASSCAN_AC
                s.statistics = STATISTICS
                s.run()
            time.sleep(60)
    except Exception, e:
        logger.error(e)


if __name__ == "__main__":
    na_start()
