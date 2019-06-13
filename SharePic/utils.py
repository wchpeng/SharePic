from django.core.cache import cache


def cache_value(CACHE_FORMAT, key, timeout=None):
    def wrapper(func):
        def inner(self, *args, **kwargs):
            val = getattr(self, key, None)
            if not val:
                return ""
            cache_key = CACHE_FORMAT.format(val)
            res = cache.get(cache_key)
            if not res:
                res = func(self, *args, **kwargs)
                if timeout:
                    cache.set(cache_key, res, timeout)
                else:
                    cache.set(cache_key, res)

            return res

        return inner

    return wrapper
