# coding: utf-8
import json
from datetime import datetime
from hashlib import sha1
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.exceptions import Throttled
# 自定义接口访问频率控制


class UserBurstRateThrottle(UserRateThrottle):
    """
    登录用户瞬时速率，如每秒100次
    """
    scope = 'user_burst'


class UserSustainedRateThrottle(UserRateThrottle):
    """
    登录用户持续访问速率，如每天1000次
    """
    scope = 'user_sustained'


class AnonBurstRateThrottle(AnonRateThrottle):
    """
    匿名用户瞬时速率，如每秒10次
    """
    scope = 'anon_burst'


class AnonSustainedRateThrottle(UserRateThrottle):
    """
    匿名用户持续访问速率，如每天1000次
    """
    scope = 'anon_sustained'


class ActionThrottled(Throttled):
    """
    :exception
    """
    pass


def rate_limit(cache, key, decrement=1, maximum_stamina=5, regenerate_per_hour=60):
    """
    接口操作限制
    默认最大尝试5次，每1分钟增加一次, 5分钟恢复

    ref: github:bradbeattie/django-cache-throttle

    The cache entry _key_ can never have more points than _maximum_stamina_.
    When points are decremented via _decrement_, they're regenerated at the
    rate of _regenerate_per_hour_. With _regenerate_per_hour_ set to 900,
    that means one point per 4 seconds. If the stored number of points ever
    reaches the maximum_stamina, we don't bother storing it in the cache
    anymore and assume that any uncached entry has _maximum_stamina_ points.

    :param cache:
    :param key:
    :param decrement:
    :param maximum_stamina:
    :param regenerate_per_hour:
    :return:
    """

    # Convert the given key into something hashable
    key = "throttle:%s" % sha1(json.dumps(key)).hexdigest()

    # Determine the current stamina
    entry = cache.get(key)
    if entry is None:
        current_stamina = maximum_stamina
    else:
        current_stamina = min(
            maximum_stamina,
            entry[0] + (datetime.now() - entry[1]).total_seconds() * (regenerate_per_hour / 3600.0)
        )

    # Decrement the current stamina and choke if it's too low
    current_stamina -= decrement
    print(current_stamina)
    if current_stamina < 0:
        cache.set(
            key,
            (-4, datetime.now()),
            3600.0 * (maximum_stamina - 0) / regenerate_per_hour
        )
        return -1
        # raise ActionThrottled(current_stamina + decrement)

    # Note the success by storing the newly decreased stamina
    cache.set(
        key,
        (current_stamina, datetime.now()),
        3600.0 * (maximum_stamina - current_stamina) / regenerate_per_hour
    )
    return current_stamina
