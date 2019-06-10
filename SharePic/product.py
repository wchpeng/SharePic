# 生产环境配置

from SharePic.settings import *  # NOQA

DEBUG = False

# config cache to use redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/11',
        # 'LOCATION': 'redis://172.16.15.203:6379/11',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # 'PASSWORD': 'my secret',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COLLECTION_POOL_KWARGS': {'max_collections': 100}
        }
    }
}

# config session to use redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

STATIC_ROOT = '/var/www/wcp/SharePic/static'
MEDIA_ROOT = '/var/www/wcp/SharePic/media'
