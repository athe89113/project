# coding=utf-8
from init import VERSION


def string_version_to_tuple(version):
    """
    v2.24.2 => ('major', 'minor', 'micro', 'releaselevel', 'serial')
    :param version:
    :return:
    """
    version = tuple([int(i) for i in version[1:].split('.')])
    return version


def get_version(version=VERSION, type='string'):
    """
    获取版本
    :param version: tuple of ('major', 'minor', 'micro', 'releaselevel', 'serial')
    :param type:
            string => v2.24.2
            int    => 22402
    :return:
    """

    if not isinstance(version, tuple):
        version = string_version_to_tuple(version)

    # get from changelog
    # with open("CHANGELOG.md") as f:
    #     first_line = f.readline()
    #     match = re.search('v[0-9.]+', first_line)
    #     print(match.start(), match.end())
    #     version = first_line[match.start():match.end()]

    if type == 'int':
        return get_int_version(version)
    else:
        return get_string_version(version)


def get_string_version(version=VERSION):
    """
    :param version: tuple of ('major', 'minor', 'micro', 'releaselevel', 'serial')
    :return:
    """
    return "v" + '.'.join(str(x) for x in version[:3])


def get_int_version(version=VERSION):
    """
    获取版本
    :param version: tuple of ('major', 'minor', 'micro', 'releaselevel', 'serial')
    :return:
    """
    major_int = 10000 * version[0] + 100 * version[1] + 1 * version[2]
    return major_int
