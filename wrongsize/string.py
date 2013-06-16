import re


def un_camel(s):
    """CamelCaseの文字列をunder_line形式に変換する。"""

    rslt = s[0].lower() + s[1:]
    def func(m):
        return '_' + m.group(0).lower()
    return re.sub(r'[A-Z]', func, rslt)


def split_camel(s, sep=' '):
    """CamelCaseの文字列を分割する。

    * *s* 文字列
    * *sep* セパレーター
    """

    def func(m):
        return sep + m.group(0)
    return s[0] + re.sub(r'[A-Z]', func, s[1:])
