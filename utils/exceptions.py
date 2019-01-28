# coding=utf-8
"""异常
"""


class AdminPasswordException(Exception):
    """
    密码错误
    """


class AdminPasswordThrottled(Exception):
    """
    密码次数过多
    """


class SocException(Exception):
    """
    通用异常
    """


class NoSocAgentException(SocException):
    """
    无soc agent 异常

    在无可用soc agent时会导致底层的一些操作无法继续进行
    """


class NotSupportedError(SocException):
    """不支持或者暂时未支持
    """
