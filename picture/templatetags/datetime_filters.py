from datetime import datetime

from django.template import Library

register = Library()


@register.filter(name="datetime_semantization")
def datetime_semantization(dt):
    # 把传入的时间格式化显示
    secs = (datetime.now() - dt).total_seconds()

    if secs < 60:
        return "%d 秒之前" % secs
    elif secs <= 3600:
        return "%d 分钟之前" % (secs//60)
    elif secs <= 86400:
        return "%d 小时 %d 分钟之前" % (secs//3600, secs % 3600//60)
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


@register.filter(name="limit_str_len")
def limit_str_len(s, length):
    # 对文字的长度做处理（一个汉字占两个英文字母位，传入的 length 是英文字母的长度）
    bs = s.encode(encoding="utf-8")
    s_len = (len(bs) + len(s))/2
    if s_len <= length:
        return s.ljust(length)
    else:
        while True:
            try:
                new_s = bs[:length].decode(encoding="utf-8")
                break
            except UnicodeDecodeError:
                length -= 1
        return new_s + "..."


@register.filter(name="replace_em")
def replace_em(s):
    import re
    s = s.replace("<", '&lt;')
    s = s.replace(">", '&gt;')
    s = s.replace("\n", '<br/>')
    s = re.sub(r'\[em_([0-9]*)\]', '<img src="{% static \'base/emoji/arclist\' %}/\g<1>.gif" border="0" />', s)
    return s
