from datetime import datetime

from django.template import Library

register = Library()


@register.filter(name="datetime_semantization")
def datetime_semantization(dt):
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
