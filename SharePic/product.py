# 生产环境配置

from SharePic.settings import *  # NOQA

DEBUG = False

# config cache to use redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/11",
        # 'LOCATION': 'redis://172.16.15.203:6379/11',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 'PASSWORD': 'my secret',
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "COLLECTION_POOL_KWARGS": {"max_collections": 100},
        },
    }
}

# config session to use redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

STATIC_ROOT = "/var/www/wcp/SharePic/static"
MEDIA_ROOT = "/var/www/wcp/SharePic/media"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s"
        }  # 日志格式
    },
    "filters": {},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/home/wcp/var/logs/SharePic_default.log",  # 日志输出文件
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份份数
            "formatter": "standard",  # 使用哪种formatters日志格式
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/home/wcp/var/logs/SharePic_error.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "request_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/home/wcp/var/logs/SharePic_request.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
        },
        "scprits_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/home/wcp/var/logs/SharePic_script.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["default", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["request_handler"],
            "level": "DEBUG",
            "propagate": False,
        },
        "scripts": {
            "handlers": ["scprits_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "sourceDns.webdns.views": {
            "handlers": ["default", "error"],
            "level": "DEBUG",
            "propagate": True,
        },
        "sourceDns.webdns.util": {
            "handlers": ["error"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
