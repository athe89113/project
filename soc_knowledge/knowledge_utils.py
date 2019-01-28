# coding=utf-8

def get_level(vul_obj):
    """ 获取漏洞级别
    :param vul_obj:
    :return:
    """

    score = vul_obj.score
    if score:
        score = float(score)
        # 默认B级厂商评分
        # low 0-4 medium 4-7 high 7-9 critical 9-10
        if 0 <= score < 4:
            level = 1
        elif 4 <= score < 7:
            level = 2
        elif 7 <= score < 9:
            level = 3
        elif 9 <= score <= 10:
            level = 4
        else:
             level = 1
    else:
        lv = {
            u'超': 4,
            u'高': 3,
            u'中': 2,
            u'低': 1,
            '--': 1
        }
        vul_lv = vul_obj.vul_level or '--'
        level = 1
        for k in lv:
            if k in vul_lv:
                level = lv[k]
                break
    return level


def get_data_source(flag):
    """ 获取漏洞数据来源类别
    :param flag: 1 CNNVD 2 CNVD 3 CVE
    :return:
    """
    source = {
        '1': u'CNNVD',
        '2': u'CNVD',
        '3': u'CVE'
    }
    flag = str(flag)
    s_name = source.get(flag, 'OTHER')
    return s_name


def get_firm_level(firm_type, score):
    """ 厂商评分级别
    :param firm_type: A厂商 B厂商 C厂商
    :return:
    """
    score = float(score)
    level = 1
    a_score = {
        '0-3.5': 1,
        '3.5-6.5': 2,
        '6.5-8.5': 3,
        '8.5-10': 4
    }
    b_score = {
        '0-4': 1,
        '4-7': 2,
        '7-9': 3,
        '9-10': 4
    }
    c_score = {
        '0-4.5': 1,
        '4.5-7.5': 2,
        '7.5-9.5': 3,
        '9.5-10': 4
    }

    score_conf = {
        'A': a_score,
        'B': b_score,
        'C': c_score
    }

    conf = score_conf[firm_type]
    for k in conf:
        rg = [float(i) for i in k.split('-')]
        if rg[0] <= score < rg[1]:
            level = conf[k]
            break
    return level
