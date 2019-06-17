# 开发环境的配置

from SharePic.settings import *  # NOQA

# config cache to use redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 'LOCATION': 'redis://127.0.0.1:6379/11',
        'LOCATION': 'redis://172.16.15.203:6379/11',
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

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = None

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# celery configure
CELERY_BROKER_URL = 'redis://172.16.15.203/12'
CELERY_RESULT_BACKEND = 'redis://172.16.15.203/12'
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/12'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/12'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}